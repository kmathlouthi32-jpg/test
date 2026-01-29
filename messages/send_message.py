import asyncio
import random
import os
from datetime import datetime, timedelta

import pytz
from telethon import TelegramClient, errors
from telethon.errors import ChatSendMediaForbiddenError

# ================= CONFIG =================

api_id = 23317696
api_hash = "33e303d5ccaed2a5f0d8eb1a1ca974d1"
session_name = "merooxx"

TZ = pytz.timezone("US/Eastern")
MAX_SAVED_MSGS = 100

FILES = {
    "video": "messages/video_caption.txt",
    "photo": "messages/photo_caption.txt",
    "text":  "messages/text_only.txt",
}

# ==========================================


def load_group_names(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


async def collect_saved_messages(client):
    """Collect fresh Saved Messages every run"""
    saved = await client.get_entity("me")

    videos, photos, texts = [], [], []

    async for msg in client.iter_messages(saved, limit=MAX_SAVED_MSGS):
        if msg.video:
            videos.append(msg)
        elif msg.photo:
            photos.append(msg)
        elif msg.text:
            texts.append(msg)

    return videos, photos, texts


async def send_media_safe(client, entity, msg, media_type, title):
    """
    Download + reupload media (NO expired references)
    """
    try:
        file_path = await client.download_media(msg)

        await client.send_file(
            entity,
            file_path,
            caption=msg.text or ""
        )

        print(f"{media_type} → {title}")

    except ChatSendMediaForbiddenError:
        if msg.text:
            await client.send_message(entity, msg.text)
            print(f"📝 FALLBACK TEXT → {title}")

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


async def main(client):
    print("✅ Running daily task...")

    video_groups = load_group_names(FILES["video"])
    photo_groups = load_group_names(FILES["photo"])
    text_groups  = load_group_names(FILES["text"])

    videos, photos, texts = await collect_saved_messages(client)
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
                await send_media_safe(client, entity, msg, "🎥 VIDEO", title)

            # 🖼 PHOTO
            elif title in photo_groups and photos:
                msg = random.choice(photos)
                await send_media_safe(client, entity, msg, "🖼 PHOTO", title)

            # 📝 TEXT
            elif title in text_groups and texts:
                msg = random.choice(texts)
                await client.send_message(entity, msg.text)
                print(f"📝 TEXT → {title}")

        except errors.FloodWaitError as e:
            print(f"⏳ FloodWait {e.seconds}s → {title}")
            await asyncio.sleep(e.seconds)

        except errors.ChatWriteForbiddenError:
            print(f"❌ NO WRITE PERMISSION → {title}")

        except Exception as e:
            print(f"❌ FAILED → {title} ({type(e).__name__})")

        await asyncio.sleep(random.randint(25, 60))

    print("🔥 Daily task completed\n")


async def daily_job(client):
    while True:
        now = datetime.now(TZ)
        target = now.replace(hour=10, minute=0, second=0, microsecond=0)

        if now >= target:
            target += timedelta(days=1)

        sleep_seconds = (target - now).total_seconds()
        print(f"⏰ Next run at {target}")
        await asyncio.sleep(sleep_seconds)

        await main(client)


async def start_telethon_worker():
    async with TelegramClient(
        session_name,
        api_id,
        api_hash,
        receive_updates=False
    ) as client:
        print("🚀 Telethon worker started (updates disabled)")
        await daily_job(client)
)




