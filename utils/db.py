import asyncpg
import asyncio
from datetime import datetime, timedelta
import random, string

# --- CONFIG ---
POOL: asyncpg.Pool = None

DATABASE_URL = 'postgresql://postgres.aoddcnsgkkowtbktnske:DragonOTPbot123@aws-1-eu-north-1.pooler.supabase.com:6543/postgres'


# -------------------------------
# 🧩 CONNECTION SETUP
# -------------------------------
async def init_db():
    """Initialize a global async connection pool."""
    global POOL
    if POOL is None:
        POOL = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=3,
            command_timeout=30,
            statement_cache_size=0,  # ✅ prevents DuplicatePreparedStatementError
            max_inactive_connection_lifetime=300  # optional
        )


# -------------------------------
# 📦 TABLE CREATION
# -------------------------------


async def create_tables():
    """Create all required tables."""
    async with POOL.acquire() as conn:
        # Users table
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            banned BOOLEAN DEFAULT FALSE,
            expiry_date TEXT DEFAULT 'N/A',
            last_call TEXT DEFAULT 'N/A',
            voice TEXT DEFAULT 'Michael',
            custom_script TEXT DEFAULT 'N/A'
        );
        """)
        # Keys table
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            used BOOLEAN DEFAULT FALSE,
            key_type TEXT
        );
        """)


# -------------------------------
# 👤 USER OPERATIONS
# -------------------------------

ALLOWED_COLUMNS = {
    "user_id", "banned", "expiry_date", "last_call", "voice", "custom_script",
    'rep'
}


async def add_user(user_id: int):
    async with POOL.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (User_id)
            VALUES ($1)
            ON CONFLICT (User_id) DO NOTHING
        """, user_id)


async def set_user_value(user_id: int, col: str, value):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column name")
    async with POOL.acquire() as conn:
        await conn.execute(f"UPDATE users SET {col} = $1 WHERE User_id = $2",
                           value, user_id)


async def get_user_info(user_id: int, col: str):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column name")
    async with POOL.acquire() as conn:
        row = await conn.fetchrow(
            f"SELECT {col} FROM users WHERE User_id = $1", user_id)
        return row[col] if row else None


async def user_exists(user_id: int):
    async with POOL.acquire() as conn:
        row = await conn.fetchrow("SELECT 1 FROM users WHERE User_id = $1",
                                  user_id)
        return bool(row)


async def get_user_count():
    async with POOL.acquire() as conn:
        row = await conn.fetchrow("SELECT COUNT(*) AS count FROM users")
        return row["count"]


# -------------------------------
# 🔑 KEYS OPERATIONS
# -------------------------------

import random
import string
from datetime import datetime, timedelta

KEY_TYPES = {'2 hours', '1 day', '4 days', '1 week', '1 month'}

DURATION_MAP = {
    '2 hours': (timedelta(hours=2), '2 Hours'),
    '1 day': (timedelta(days=1), '1 Day'),
    '4 days': (timedelta(days=4), '4 Days'),
    '1 week': (timedelta(days=7), '1 Week'),
    '1 month': (timedelta(days=30), '1 Month'),
}

# -------------------------------
# 🔑 KEY UTILITIES
# -------------------------------


def random_segment(length=20):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_key():
    return f"DragonOTP-{random_segment()}"


async def generate_new_key(conn, key_type: str):
    """Generate and insert a single key of a given type."""
    new_key = generate_key()
    await conn.execute(
        "INSERT INTO keys (Key, Key_Type, Used) VALUES ($1, $2, FALSE)",
        new_key, key_type)
    return new_key


async def generate_bulk_keys(pool=POOL, total_per_duration=10):
    """Generate multiple new keys for all durations."""
    durations = DURATION_MAP.keys()

    # Ensure pool exists
    global POOL
    if pool is None:
        await init_db()
        pool = POOL  # ✅ reassign after init

    async with pool.acquire() as conn:
        async with conn.transaction():
            for duration in durations:
                for _ in range(total_per_duration):
                    key = generate_key()
                    try:
                        await conn.execute(
                            "INSERT INTO keys (Key, Key_Type, Used) VALUES ($1, $2, FALSE)",
                            key, duration)
                    except Exception:
                        pass  # Skip duplicates silently
    return "✅ Keys generated and added."


# -------------------------------
# 🔍 KEY CHECKING
# -------------------------------


async def show_valid_keys(key_type):
    if key_type not in KEY_TYPES:
        return ['❌ Invalid key type.']
    async with POOL.acquire() as conn:
        rows = await conn.fetch(
            "SELECT Key FROM keys WHERE Key_Type=$1 AND Used=FALSE", key_type)
        return [fr"`{r['key']}`"
                for r in rows] if rows else [r"⚠️ No available keys\."]


# -------------------------------
# ⏱️ KEY REDEMPTION LOGIC
# -------------------------------


async def redeem_key(user_id: int, key: str):
    """Redeem a key, extend expiry, mark used, and auto-generate new key of same type."""
    async with POOL.acquire() as conn:
        if key == 'DragonOTP-93J9YHKT8DKMXJC9YCRY':
            if await get_user_info(user_id, 'rep') == True:
                return '❌ The Repport Calls are Already Unlocked!'
            await set_user_value(user_id, 'rep', True)
            return '✅ Repport Calls Unlocked Successfully!'
        key_row = await conn.fetchrow(
            "SELECT Key_Type, Used FROM keys WHERE Key=$1", key)
        if not key_row:
            return '❌ Invalid or Unknown Key!'
        if key_row["used"]:
            return '❌ This key has already been used!'

        key_type_code = key_row["key_type"]
        if key_type_code not in DURATION_MAP:
            return '❌ Invalid Key Format!'

        duration, label = DURATION_MAP[key_type_code]
        expiry_str = await get_user_info(user_id, 'expiry_date')
        now = datetime.now()

        # Determine if user is new or already has valid subscription
        try:
            exp_dt = datetime.strptime(
                expiry_str,
                "%Y-%m-%d %H:%M:%S.%f") if expiry_str != 'N/A' else now
        except Exception:
            exp_dt = now

        current_expiry = now if exp_dt < now else exp_dt
        new_expiry = current_expiry + duration

        # Update user expiry
        await set_user_value(user_id, 'expiry_date', str(new_expiry))

        # Mark key as used
        await conn.execute("UPDATE keys SET Used=TRUE WHERE Key=$1", key)

        # Generate replacement key of same type
        await generate_new_key(conn, key_type_code)

        return f'✅ {label} Key Redeemed Successfully!'


# -------------------------------
# 🧪 TEST RUN (for local dev)
# -------------------------------
if __name__ == "__main__":

    async def main():
        await init_db()
        await create_tables()
        print("Database ready ✅")

    asyncio.run(main())

