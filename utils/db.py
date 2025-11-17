import asyncpg
import asyncio
from datetime import datetime, timedelta
import random, string

# --- CONFIG ---
POOL: asyncpg.Pool = None
DATABASE_URL = 'postgresql://postgres.aoddcnsgkkowtbktnske:dragonotp.bot1234.@aws-1-eu-north-1.pooler.supabase.com:6543/postgres'


# ============================
#  SAFE DB INITIALIZATION
# ============================

async def init_db():
    """Initialize a global async connection pool."""
    global POOL
    if POOL is not None:
        return

    POOL = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=5,
        max_inactive_connection_lifetime=30,  # 🔥 auto-refresh stale connections
        command_timeout=30,
        statement_cache_size=0
    )


# ============================
#  SAFE QUERY WRAPPER
# ============================

async def safe_query(func, *args, **kwargs):
    """
    Executes DB operations with automatic reconnection.
    """
    global POOL
    try:
        async with POOL.acquire() as conn:
            return await func(conn, *args, **kwargs)

    except asyncpg.exceptions.ConnectionDoesNotExistError:
        print("⚠️ Connection died — rebuilding pool...")
        POOL = None
        await init_db()
        async with POOL.acquire() as conn:
            return await func(conn, *args, **kwargs)


# ============================
#  TABLE CREATION
# ============================

async def create_tables():
    async def _create(conn):
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            banned BOOLEAN DEFAULT FALSE,
            expiry_date TEXT DEFAULT 'N/A',
            last_call TEXT DEFAULT 'N/A',
            voice TEXT DEFAULT 'Michael',
            custom_script TEXT DEFAULT 'N/A',
            rep BOOLEAN DEFAULT FALSE
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            used BOOLEAN DEFAULT FALSE,
            key_type TEXT
        );
        """)

    return await safe_query(_create)


# ============================
#  USER OPERATIONS
# ============================

ALLOWED_COLUMNS = {
    "user_id", "banned", "expiry_date",
    "last_call", "voice", "custom_script", "rep"
}

async def add_user(user_id: int):
    async def _add(conn):
        return await conn.execute("""
            INSERT INTO users (user_id)
            VALUES ($1)
            ON CONFLICT (user_id) DO NOTHING
        """, user_id)

    return await safe_query(_add)


async def set_user_value(user_id: int, col: str, value):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column")

    async def _set(conn):
        return await conn.execute(
            f"UPDATE users SET {col} = $1 WHERE user_id=$2",
            value, user_id
        )

    return await safe_query(_set)


async def get_user_info(user_id: int, col: str):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column")

    async def _get(conn):
        row = await conn.fetchrow(
            f"SELECT {col} FROM users WHERE user_id=$1", user_id
        )
        return row[col] if row else None

    return await safe_query(_get)


async def user_exists(user_id: int):
    async def _exists(conn):
        row = await conn.fetchrow(
            "SELECT 1 FROM users WHERE user_id=$1", user_id
        )
        return bool(row)

    return await safe_query(_exists)


async def get_user_count():
    async def _count(conn):
        row = await conn.fetchrow("SELECT COUNT(*) AS count FROM users")
        return row["count"]

    return await safe_query(_count)


# ============================
#  KEY UTILITIES
# ============================

KEY_TYPES = {'2 hours', '1 day', '4 days', '1 week', '1 month'}

DURATION_MAP = {
    '2 hours': (timedelta(hours=2), '2 Hours'),
    '1 day': (timedelta(days=1), '1 Day'),
    '4 days': (timedelta(days=4), '4 Days'),
    '1 week': (timedelta(days=7), '1 Week'),
    '1 month': (timedelta(days=30), '1 Month'),
}

def random_segment(length=20):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_key():
    return f"DragonOTP-{random_segment()}"


# ============================
#  KEY GENERATION
# ============================

async def generate_new_key(conn, key_type: str):
    """Generate and insert a single key of a given type."""
    new_key = generate_key()
    await conn.execute(
        "INSERT INTO keys (key, key_type, used) VALUES ($1, $2, FALSE)",
        new_key, key_type
    )
    return new_key


async def generate_bulk_keys(total_per_duration=10):
    async def _bulk(conn):
        for duration in DURATION_MAP.keys():
            for _ in range(total_per_duration):
                try:
                    await conn.execute(
                        "INSERT INTO keys (key, key_type, used) VALUES ($1, $2, FALSE)",
                        generate_key(), duration
                    )
                except Exception:
                    pass

    return await safe_query(_bulk)


# ============================
#  KEY CHECKING
# ============================

async def show_valid_keys(key_type):
    if key_type not in KEY_TYPES:
        return ['❌ Invalid key type.']

    async def _show(conn):
        rows = await conn.fetch(
            "SELECT key FROM keys WHERE key_type=$1 AND used=FALSE",
            key_type
        )
        return [f"`{r['key']}`" for r in rows] if rows else ["⚠️ No available keys."]

    return await safe_query(_show)


# ============================
#  KEY REDEMPTION
# ============================

async def redeem_key(user_id: int, key: str):
    async def _redeem(conn):

        # special key
        if key == 'DragonOTP-93J9YHKT8DKMXJC9YCRY':
            rep = await get_user_info(user_id, "rep")
            if rep:
                return "❌ The Report Calls are already unlocked."
            await set_user_value(user_id, "rep", True)
            return "✅ Report Calls Unlocked!"

        row = await conn.fetchrow(
            "SELECT key_type, used FROM keys WHERE key=$1", key
        )

        if not row:
            return "❌ Invalid key."
        if row["used"]:
            return "❌ Key already used."

        key_type_code = row["key_type"]
        if key_type_code not in DURATION_MAP:
            return "❌ Invalid key type."

        duration, label = DURATION_MAP[key_type_code]

        expiry_str = await get_user_info(user_id, "expiry_date")
        now = datetime.now()

        try:
            exp_dt = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S.%f") if expiry_str != 'N/A' else now
        except:
            exp_dt = now

        current_exp = now if exp_dt < now else exp_dt
        new_expiry = current_exp + duration

        await set_user_value(user_id, "expiry_date", str(new_expiry))
        await conn.execute("UPDATE keys SET used=TRUE WHERE key=$1", key)
        await generate_new_key(conn, key_type_code)

        return f"✅ {label} Key Redeemed Successfully!"

    return await safe_query(_redeem)


# ============================
#  LOCAL TEST
# ============================

if __name__ == "__main__":
    async def main():
        await init_db()
        await create_tables()
        print("Database is ready.")

    asyncio.run(main())

