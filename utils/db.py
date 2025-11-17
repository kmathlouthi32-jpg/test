import asyncpg
import asyncio
from datetime import datetime, timedelta
import random, string

# --- CONFIG ---
POOL: asyncpg.Pool = None
POOL_LOCK = asyncio.Lock()
DATABASE_URL = 'postgresql://postgres:dragonotp.bot1234.@aws-1-eu-north-1.pooler.supabase.com:6543/postgres'

# ============================
# SAFE DB INITIALIZATION
# ============================

async def init_db():
    """Initialize a global async connection pool safely."""
    global POOL
    async with POOL_LOCK:
        if POOL is not None:
            return
        try:
            POOL = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=1,
                max_size=5,
                max_inactive_connection_lifetime=30,
                command_timeout=30,
                statement_cache_size=0
            )
            print("✅ Database pool created successfully.")
        except Exception as e:
            print(f"❌ Failed to create DB pool: {e}")
            POOL = None

# ============================
# SAFE QUERY WRAPPER
# ============================

async def safe_query(func, *args, **kwargs):
    global POOL
    if POOL is None:
        await init_db()
        if POOL is None:
            raise RuntimeError("Database connection pool is not available.")

    try:
        async with POOL.acquire() as conn:
            return await func(conn, *args, **kwargs)
    except (asyncpg.exceptions.ConnectionDoesNotExistError,
            asyncpg.exceptions.InterfaceError,
            ConnectionError) as e:
        print(f"⚠️ Connection lost: {e}. Reconnecting...")
        POOL = None
        await init_db()
        if POOL is None:
            raise RuntimeError("Database pool unavailable after reconnect.")
        async with POOL.acquire() as conn:
            return await func(conn, *args, **kwargs)

# ============================
# TABLE CREATION
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
# USER OPERATIONS
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

async def get_user_info(user_id: int, col: str):
    if col not in ALLOWED_COLUMNS:
        raise ValueError("Invalid column")

    async def _get(conn):
        row = await conn.fetchrow(f"SELECT {col} FROM users WHERE user_id=$1", user_id)
        return row[col] if row else None

    return await safe_query(_get)

# ============================
# KEY UTILITIES
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
# EXAMPLE: TEST DB
# ============================

if __name__ == "__main__":
    async def main():
        await init_db()
        await create_tables()
        print("Database ready ✅")

    asyncio.run(main())
