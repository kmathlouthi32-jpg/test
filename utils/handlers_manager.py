from .database import db

USER_CACHE = {}

async def load_all_users():
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")

    for row in rows:
        USER_CACHE[row["user_id"]] = dict(row)

    print(f"⚡ Loaded {len(USER_CACHE)} users into RAM")

def is_new_user(user_id:int):
    if user_id not in USER_CACHE:
        return True, len(USER_CACHE)+1
    return False, len(USER_CACHE)

def get_user_cached(user_id: int):
    return USER_CACHE.get(user_id)

async def add_user_fast(user_id: int):
    await db.add_user(user_id)
    USER_CACHE[user_id] = {
        "user_id": user_id,
        "banned": False,
        "expiry_date": "N/A",
        "last_call": "N/A",
        "voice": "Michael",
        "custom_script": "N/A",
        "rep": False,
        "wallet": 0
    }

async def update_user_cache(user_id: int, field: str, value):
    USER_CACHE[user_id][field] = value
    await db.set_user_value(user_id, field, value)

def get_all_users():
    return [user_id for user_id, data in USER_CACHE.items() if not data.get("banned", False)]


