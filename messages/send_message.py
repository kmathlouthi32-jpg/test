import asyncio
from datetime import datetime, timedelta
import pytz
import random
from telethon import TelegramClient, errors
from telethon.errors import ChatSendMediaForbiddenError

api_id = 23317696
api_hash = "33e303d5ccaed2a5f0d8eb1a1ca974d1"
session_name = "merooxx"

# Timezone for USA Eastern Time
TZ = pytz.timezone("US/Eastern")

# Max messages to load from Saved Messages
MAX_SAVED_MSGS = 100

# Message files for different types
FILES = {
    "video": "messages/video_caption.txt",
    "photo": "messages/photo_caption.txt",
    "text": "messages/text_only.txt"
}

# ================================================

def load_group_names(filename):
    """Load group titles from a file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()


async def main(client):
    """Send messages to groups based on Saved Messages"""
    print("✅ Running daily task...")

    video_groups = load_group_names(FILES["video"])
    photo_groups = load_group_names(FILES["photo"])
    text_groups  = load_group_names(FILES["text"])

    saved = await client.get_entity("me")
    videos, photos, texts = [], [], []

    async for msg in client.iter_messages(saved, limit=MAX_SAVED_MSGS):
        if msg.video:
            videos.append(msg)
        elif msg.photo:
            photos.append(msg)
        elif msg.text:
            texts.append(msg)

    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        entity = dialog.entity
        title = getattr(entity, "title", None)
        if not title:
            continue

        try:
            # 🎥 VIDEO
            if title in video_groups and videos:
                msg = random.choice(videos)
                try:
                    await client.send_file(entity, msg.media, caption=msg.text or "")
                    print(f"🎥 VIDEO → {title}")
                except ChatSendMediaForbiddenError:
                    if msg.text:
                        await client.send_message(entity, msg.text)
                        print(f"📝 FALLBACK TEXT → {title}")

            # 🖼 PHOTO
            elif title in photo_groups and photos:
                msg = random.choice(photos)
                try:
                    await client.send_file(entity, msg.media, caption=msg.text or "")
                    print(f"🖼 PHOTO → {title}")
                except ChatSendMediaForbiddenError:
                    if msg.text:
                        await client.send_message(entity, msg.text)
                        print(f"📝 FALLBACK TEXT → {title}")

            # 📝 TEXT
            elif title in text_groups and texts:
                msg = random.choice(texts)
                await client.send_message(entity, msg.text)
                print(f"📝 TEXT → {title}")

        except errors.FloodWaitError as e:
            print(f"⏳ FloodWait {e.seconds}s for {title}")
            await asyncio.sleep(e.seconds)

        except errors.ChatWriteForbiddenError:
            print(f"❌ NO WRITE PERMISSION → {title}")

        except Exception as e:
            print(f"❌ FAILED → {title} ({type(e).__name__})")

        # Random delay to avoid spam detection
        await asyncio.sleep(random.randint(20, 60))

    print("🔥 Daily task completed\n")


async def daily_job(client):
    """Run the task every day at 06:34 USA Eastern time"""
    while True:
        now = datetime.now(TZ)
        target = now.replace(hour=6, minute=39, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)

        sleep_seconds = (target - now).total_seconds()
        print(f"⏰ Next run at {target} (sleeping {sleep_seconds:.0f}s)")
        await asyncio.sleep(sleep_seconds)

        # Run the sending task
        await main(client)


async def start_telethon_worker():
    """Start the Telethon client and schedule the daily job"""
    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("🚀 Telethon worker started")
        try:
            await daily_job(client)
        except asyncio.CancelledError:
            print("🛑 Telethon worker stopped cleanly")
        except Exception as e:
            print(f"❌ Telethon worker crashed: {e}")




