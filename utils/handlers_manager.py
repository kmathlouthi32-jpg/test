from .database import db
import asyncio

# =========================
# GLOBAL CACHE + LOCK
# =========================
USER_CACHE = {}
USER_CACHE_LOCK = asyncio.Lock()

# =========================
# LOAD / RELOAD USERS
# =========================
async def load_all_users():
    # Clear cache safely
    async with USER_CACHE_LOCK:
        USER_CACHE.clear()

    # Load from DB
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")

    # Repopulate cache safely
    async with USER_CACHE_LOCK:
        for row in rows:
            USER_CACHE[row["user_id"]] = dict(row)

    print(f"♻️ Reloaded {len(USER_CACHE)} users into RAM")


async def reload_users_every_12h():
    while True:
        await asyncio.sleep(12 * 60 * 60)  # 12 hours
        print("⏳ 12h reached → reloading users")
        await load_all_users()

# =========================
# USER HELPERS
# =========================
def is_new_user(user_id: int):
    return user_id not in USER_CACHE


def get_user_cached(user_id: int):
    return USER_CACHE.get(user_id)


async def add_user_fast(user_id: int):
    await db.add_user(user_id)

    async with USER_CACHE_LOCK:
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
    async with USER_CACHE_LOCK:
        if user_id not in USER_CACHE:
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

        USER_CACHE[user_id][field] = value

    # DB is source of truth
    await db.set_user_value(user_id, field, value)


def get_all_users():
    return [
        user_id
        for user_id, data in USER_CACHE.items()
        if not data.get("banned", False)
    ]
