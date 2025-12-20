from .database import db
import time


# --------------------------
# In-memory cache
# --------------------------
USER_CACHE = {}
CACHE_LOADED = False

async def load_all_users():
    """
    Load all users into memory cache at startup.
    """
    global USER_CACHE, CACHE_LOADED
    await db.init_db()
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
        for row in rows:
            USER_CACHE[row["user_id"]] = {
                "banned": row["banned"],
                "expiry_date": row["expiry_date"],
                "last_call": row["last_call"],
                "voice": row["voice"],
                "custom_script": row["custom_script"],
                "rep": row["rep"],
                "wallet":row['wallet']
            }
    CACHE_LOADED = True
    print(f"✅ Loaded {len(USER_CACHE)} users into memory cache.")

async def is_new_user(user_id:int):
    if user_id not in USER_CACHE:
        return True, len(USER_CACHE)+1
    return False, len(USER_CACHE)

async def get_user_cached(user_id: int):
    """
    Get user info from cache. Auto-add if not exists.
    """
    global USER_CACHE

    # Lazy-load all users on first call if not done
    if not CACHE_LOADED:
        await load_all_users()

    now = time.time()
    # Check cache
    if user_id in USER_CACHE:
        return USER_CACHE[user_id]

    # User not in cache -> add to DB & cache
    await db.add_user(user_id)
    USER_CACHE[user_id] = {
        "banned": False,
        "expiry_date": "N/A",
        "last_call": "N/A",
        "voice": "Michael",
        "custom_script": "N/A",
        "rep": False,
        'wallet':1

    }
    return USER_CACHE[user_id]

async def update_user_cache(user_id: int, field: str, value):
    """
    Update in-memory cache and DB.
    """
    if user_id not in USER_CACHE:
        await get_user_cached(user_id)

    USER_CACHE[user_id][field] = value
    await db.set_user_value(user_id, field, value)

async def get_all_users():
    return [user_id for user_id, data in USER_CACHE.items() if not data.get("banned", False)]

