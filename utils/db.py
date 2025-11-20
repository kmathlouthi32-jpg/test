import asyncpg
import asyncio
from datetime import datetime, timedelta
import random
import string

# -----------------------------------
# 🔧 DATABASE CONFIG
# -----------------------------------

POOL: asyncpg.Pool = None

DATABASE_URL = (
    'postgresql://postgres.aoddcnsgkkowtbktnske:DragonOTPbot123@aws-1-eu-north-1.pooler.supabase.com:6543/postgres'
)

# -----------------------------------
# 🔌 SAFE DB INITIALIZATION
# -----------------------------------

async def init_db():
    """
    Initialize asyncpg connection pool with retry logic.
    Fixes: ConnectionDoesNotExistError on Render/Supabase cold start.
    """
    global POOL
    if POOL is not None:
        return POOL  # Pool already exists

    retries = 5
    for attempt in range(1, retries + 1):
        try:
            POOL = await asyncpg.create_pool(
                dsn=DATABASE_URL,
                min_size=1,
                max_size=3,
                command_timeout=30,
                statement_cache_size=0,
                max_inactive_connection_lifetime=300,
            )
            print("🔥 DB Connected Successfully")
            return POOL

        except Exception as e:
            print(f"❌ DB connection failed (attempt {attempt}/5): {e}")

            if attempt == retries:
                print("❌ Could not connect to DB after 5 attempts.")
                raise e

            await asyncio.sleep(2)

    return POOL


# -----------------------------------
# 📦 TABLE CREATION
# -----------------------------------

async def create_tables():
    await init_db()

    async with POOL.acquire() as conn:
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


# -----------------------------------
# 👤 USER OPERATIONS
# -----------------------------------

ALLOWED_COLUMNS = {
    "user_id", "banned", "expiry_date", "last_call", "voice",
    "custom_script", "rep"
}


async def add_user(user_id: int):
    await init_db()
    async with POOL.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id)
            VALUES ($1)
            ON CONFLICT (user_id) DO NOTHING
            """, user_id
        )


async def set_user_value(user_id: int, col: str, value):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column name")

    await init_db()
    async with POOL.acquire() as conn:
        await conn.execute(
            f"UPDATE users SET {col} = $1 WHERE user_id = $2",
            value, user_id
        )


async def get_user_info(user_id: int, col: str):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column name")

    await init_db()
    async with POOL.acquire() as conn:
        row = await conn.fetchrow(
            f"SELECT {col} FROM users WHERE user_id=$1",
            user_id
        )
        return row[col] if row else None


async def user_exists(user_id: int):
    await init_db()
    async with POOL.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT 1 FROM users WHERE user_id=$1", user_id
        )
        return bool(row)


async def get_user_count():
    await init_db()
    async with POOL.acquire() as conn:
        row = await conn.fetchrow("SELECT COUNT(*) AS count FROM users")
        return row["count"]


# -----------------------------------
# 🔑 KEYS
# -----------------------------------

KEY_TYPES = {'2 hours', '1 day', '4 days', '1 week', '1 month'}

DURATION_MAP = {
    '2 hours': (timedelta(hours=2), '2 Hours'),
    '1 day': (timedelta(days=1), '1 Day'),
    '4 days': (timedelta(days=4), '4 Days'),
    '1 week': (timedelta(days=7), '1 Week'),
    '1 month': (timedelta(days=30), '1 Month'),
}


def random_segment(length=20):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_key():
    return f"DragonOTP-{random_segment()}"


async def generate_new_key(conn, key_type: str):
    key = generate_key()
    await conn.execute(
        "INSERT INTO keys (key, key_type, used) VALUES ($1, $2, FALSE)",
        key, key_type
    )
    return key


async def generate_bulk_keys(total_per_duration=10):
    await init_db()

    async with POOL.acquire() as conn:
        async with conn.transaction():
            for duration in DURATION_MAP:
                for _ in range(total_per_duration):
                    try:
                        await conn.execute(
                            "INSERT INTO keys (key, key_type, used) VALUES ($1, $2, FALSE)",
                            generate_key(), duration
                        )
                    except:
                        pass
    return "✅ Keys generated."


async def show_valid_keys(key_type):
    if key_type not in KEY_TYPES:
        return ["❌ Invalid key type."]

    await init_db()
    async with POOL.acquire() as conn:
        rows = await conn.fetch(
            "SELECT key FROM keys WHERE key_type=$1 AND used=FALSE",
            key_type
        )
        return [f"`{r['key']}`" for r in rows] or ["⚠️ No available keys."]


# -----------------------------------
# ⏱ KEY REDEMPTION
# -----------------------------------

async def redeem_key(user_id: int, key: str):
    await init_db()

    async with POOL.acquire() as conn:

        # Special rep key
        if key == "DragonOTP-93J9YHKT8DKMXJC9YCRY":
            if await get_user_info(user_id, "rep"):
                return "❌ Rep Calls already unlocked!"
            await set_user_value(user_id, "rep", True)
            return "✅ Rep Calls Unlocked!"

        row = await conn.fetchrow(
            "SELECT key_type, used FROM keys WHERE key=$1", key
        )

        if not row:
            return "❌ Invalid key!"
        if row["used"]:
            return "❌ Key already used!"

        key_type = row["key_type"]
        if key_type not in DURATION_MAP:
            return "❌ Unknown key type!"

        duration, label = DURATION_MAP[key_type]

        now = datetime.now()
        current_exp = await get_user_info(user_id, "expiry_date")

        try:
            expiry = datetime.strptime(current_exp, "%Y-%m-%d %H:%M:%S.%f")
        except:
            expiry = now

        base = now if expiry < now else expiry
        new_expiry = base + duration

        await set_user_value(user_id, "expiry_date", str(new_expiry))
        await conn.execute("UPDATE keys SET used=TRUE WHERE key=$1", key)
        await generate_new_key(conn, key_type)

        return f"✅ {label} Key Redeemed Successfully!"
