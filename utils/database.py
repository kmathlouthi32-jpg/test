import asyncpg
import asyncio
from datetime import datetime, timedelta
import random
import string
import httpx

class DBManager:
    KEY_TYPES = {'2 hours', '1 day', '4 days', '1 week', '1 month', 'lifetime'}
    DURATION_MAP = {
    '2 hours': (timedelta(hours=2), '2 Hours'),
    '1 day': (timedelta(days=1), '1 Day'),
    '4 days': (timedelta(days=4), '4 Days'),
    '1 week': (timedelta(days=7), '1 Week'),
    '1 month': (timedelta(days=30), '1 Month'),
    'lifetime': (timedelta(days=365*1000), 'Lifetime'),
    }
    ALLOWED_COLUMNS = {
    "user_id", "banned", "expiry_date", "last_call", "voice",
    "custom_script", "rep",'wallet'
    }

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool: asyncpg.Pool = None
        self.http_client: httpx.AsyncClient = None

    # -----------------------------
    # DB & HTTP INIT
    # -----------------------------
    async def init_db(self):
        if self.pool:
            return self.pool

        retries = 5
        for attempt in range(1, retries + 1):
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=self.db_url,
                    min_size=1,
                    max_size=3,
                    command_timeout=30,
                    statement_cache_size=0,
                    max_inactive_connection_lifetime=300
                )
                print("🔥 DB Connected Successfully")
                return self.pool
            except Exception as e:
                print(f"❌ DB connection failed (attempt {attempt}/5): {e}")
                if attempt == retries:
                    raise e
                await asyncio.sleep(2)

    async def init_http_client(self):
        if not self.http_client:
            self.http_client = httpx.AsyncClient(timeout=15.0)
        return self.http_client

    # -----------------------------
    # TABLES
    # -----------------------------
    async def create_tables(self):
        await self.init_db()
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    banned BOOLEAN DEFAULT FALSE,
                    expiry_date TEXT DEFAULT 'N/A',
                    last_call TEXT DEFAULT 'N/A',
                    voice TEXT DEFAULT 'Michael',
                    custom_script TEXT DEFAULT 'N/A',
                    rep BOOLEAN DEFAULT FALSE,
                    wallet INT DEFAULT 1
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS keys (
                    key TEXT PRIMARY KEY,
                    used BOOLEAN DEFAULT FALSE,
                    key_type TEXT
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    key TEXT NOT NULL,
                    lang TEXT NOT NULL,
                    content TEXT NOT NULL,
                    PRIMARY KEY (key, lang)
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS keyboards (
                    key TEXT NOT NULL,
                    lang TEXT NOT NULL,
                    buttons JSONB NOT NULL,
                    PRIMARY KEY (key, lang)
                );
            """)

    # -----------------------------
    # USER OPERATIONS
    # -----------------------------
    async def add_user(self, user_id: int):
        await self.init_db()
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (user_id) VALUES ($1) ON CONFLICT (user_id) DO NOTHING",
                user_id
            )

    async def set_user_value(self, user_id: int, col: str, value):
        if col not in self.ALLOWED_COLUMNS:
            raise ValueError("Invalid column name")
        await self.init_db()
        async with self.pool.acquire() as conn:
            await conn.execute(f"UPDATE users SET {col}=$1 WHERE user_id=$2", value, user_id)

    async def get_user_info(self, user_id: int, col: str):
        if col not in self.ALLOWED_COLUMNS:
            raise ValueError("Invalid column name")
        await self.init_db()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(f"SELECT {col} FROM users WHERE user_id=$1", user_id)
            return row[col] if row else None

    async def user_exists(self, user_id: int):
        await self.init_db()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT 1 FROM users WHERE user_id=$1", user_id)
            return bool(row)

    async def get_user_count(self):
        await self.init_db()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT COUNT(*) AS count FROM users")
            return row["count"]

    # -----------------------------
    # KEYS
    # -----------------------------
    @staticmethod
    def random_segment(length=20):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def generate_key(self):
        return f"DragonOTP-{self.random_segment()}"

    async def generate_new_key(self, conn, key_type: str):
        key = self.generate_key()
        await conn.execute(
            "INSERT INTO keys (key, key_type, used) VALUES ($1, $2, FALSE)",
            key, key_type
        )
        return key

    async def generate_bulk_keys(self, total_per_duration=5):
        await self.init_db()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for duration in self.DURATION_MAP:
                    for _ in range(total_per_duration):
                        try:
                            await conn.execute(
                                "INSERT INTO keys (key, key_type, used) VALUES ($1, $2, FALSE)",
                                self.generate_key(), duration
                            )
                        except:
                            pass
        return "✅ Keys generated."

    async def show_valid_keys(self, key_type):
        await self.init_db()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT key FROM keys WHERE key_type=$1 AND used=FALSE",
                key_type
            )
            return [f"`{r['key']}`" for r in rows] or [r"⚠️ No available keys\."]

    # -----------------------------
    # KEY REDEMPTION
    # -----------------------------
    async def redeem_key(self, user_id: int, key: str,expiry_date: str, rep: bool):
        await self.init_db()
        async with self.pool.acquire() as conn:
            # Special rep key
            if key == "DragonOTP-93J9YHKT8DKMXJC9YCRY":
                if rep:
                    return 'norep',None
                await self.set_user_value(user_id, "rep", True)
                return 'Repport Calls',None

            row = await conn.fetchrow("SELECT key_type, used FROM keys WHERE key=$1", key)
            if not row:
                return 'wrong_key',None
            if row["used"]:
                return 'used_key',None

            key_type = row["key_type"]

            duration, label = self.DURATION_MAP[key_type]
            now = datetime.now()
            try:
                expiry = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S.%f")
            except:
                expiry = now

            base = now if expiry < now else expiry
            new_expiry = base + duration

            await conn.execute("UPDATE keys SET used=TRUE WHERE key=$1", key)
            await self.generate_new_key(conn, key_type)

            return label,new_expiry
        
    async def set_message(self, key: str, lang: str, content: str):
        await self.init_db()
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO messages (key, lang, content)
                VALUES ($1, $2, $3)
                ON CONFLICT (key, lang)
                DO UPDATE SET content = EXCLUDED.content
                """,
                key, lang, content
            )
    
    async def get_message(self, key: str, lang: str):
        await self.init_db()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT content FROM messages WHERE key=$1 AND lang=$2",
                key, lang
            )
            return row["content"] if row else None
        
    async def load_all_messages(self):
        await self.init_db()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT key, lang, content FROM messages")

        cache = {}
        for r in rows:
            cache.setdefault(r["key"], {})[r["lang"]] = r["content"]

        return cache
    
    # -----------------------------
    # KEYBOARDS
    # -----------------------------
    async def set_keyboard(self, key: str, lang: str, layout: dict):
        await self.init_db()
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO keyboards (key, lang, buttons)
                VALUES ($1, $2, $3)
                ON CONFLICT (key, lang)
                DO UPDATE SET buttons = EXCLUDED.buttons
                """,
                key, lang, layout
            )

    async def get_keyboard(self, key: str, lang: str):
        row = await self.pool.fetchrow(
            "SELECT layout FROM keyboards WHERE key=$1 AND lang=$2",
            key, lang
        )
        return row["layout"] if row else None
    
    async def load_all_keyboards(self):
        await self.init_db()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT key, lang, buttons FROM keyboards")

        cache = {}
        for r in rows:
            cache.setdefault(r["key"], {})[r["lang"]] = r["buttons"]

        return cache


DB_URL = "postgresql://postgres.aoddcnsgkkowtbktnske:DragonOTPbot123@aws-1-eu-north-1.pooler.supabase.com:6543/postgres"


db = DBManager(DB_URL)

