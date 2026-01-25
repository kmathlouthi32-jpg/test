from typing import Dict, List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .database import db
from utils.translate import fast_translate
import asyncio
import json

KEYBOARD_CACHE: Dict[str, Dict[str, List[List[dict]]]] = {}

LANG_PRELOAD_LOCKS: Dict[str, asyncio.Lock] = {}

async def load_keyboards():
    global KEYBOARD_CACHE
    keyboards = await db.load_all_keyboards()

    if not keyboards:
        print("⚠️ No keyboards found in database")
        KEYBOARD_CACHE = {}
        return

    # Make sure all entries are dicts, not JSON strings
    clean_cache = {}
    for key, langs in keyboards.items():
        clean_cache[key] = {}
        for lang, data in langs.items():
            if isinstance(data, str):
                try:
                    clean_cache[key][lang] = json.loads(data)
                except Exception:
                    clean_cache[key][lang] = {}  # fallback empty dict
            else:
                clean_cache[key][lang] = data

    KEYBOARD_CACHE = clean_cache
    print(f"⌨️ Loaded {len(KEYBOARD_CACHE)} keyboards into RAM")


SEM = asyncio.Semaphore(5)

async def safe_translate(text, lang):
    async with SEM:
        try:
            return await fast_translate(text, lang)
        except Exception:
            return text


async def preload_language_keyboard(lang: str):
    if lang == "en":
        return

    if lang not in LANG_PRELOAD_LOCKS:
        LANG_PRELOAD_LOCKS[lang] = asyncio.Lock()

    async with LANG_PRELOAD_LOCKS[lang]:

        # ✅ Check if already fully loaded
        for key in KEYBOARD_CACHE:
            if lang not in KEYBOARD_CACHE[key]:
                break
        else:
            return  # all keyboards already translated

        print(f"🌍 Preloading keyboards for language: {lang}")

        for key, langs in KEYBOARD_CACHE.items():

            if lang in langs:
                continue

            base = langs.get("en")
            if not base:
                continue

            if isinstance(base, str):
                try:
                    base = json.loads(base)
                except Exception:
                    continue

            rows = base.get("inline_keyboard")
            if not isinstance(rows, list):
                continue

            translated_keyboard = {"inline_keyboard": []}

            for row in rows:
                if not isinstance(row, list):
                    continue

                texts = []
                buttons = []

                for btn in row:
                    if isinstance(btn, dict) and "text" in btn:
                        texts.append(btn["text"])
                        buttons.append(btn)

                # 🔥 Translate row buttons in parallel
                translated_texts = await asyncio.gather(
                    *(safe_translate(t, lang) for t in texts)
                )

                new_row = []
                idx = 0

                for btn in row:
                    if not isinstance(btn, dict):
                        continue

                    new_btn = {}

                    if "text" in btn:
                        new_btn["text"] = translated_texts[idx]
                        idx += 1

                    # Preserve ONE action only
                    if "callback" in btn:
                        new_btn["callback"] = btn["callback"]
                    elif "url" in btn:
                        new_btn["url"] = btn["url"]

                    new_row.append(new_btn)

                if new_row:
                    translated_keyboard["inline_keyboard"].append(new_row)

            # 💾 Save & cache
            await db.set_keyboard(key, lang, json.dumps(translated_keyboard))
            KEYBOARD_CACHE[key][lang] = translated_keyboard

        print(f"✅ Keyboards ready for language: {lang}")


def get_keyboard_data(key: str, lang: str):
    return KEYBOARD_CACHE[key][lang]

def get_keyboard(key: str, lang: str = "en", **format_vars):
    """
    Returns Aiogram InlineKeyboardMarkup from cached keyboard.
    """
    global KEYBOARD_CACHE

    if key not in KEYBOARD_CACHE:
        return None

    keyboard_data = KEYBOARD_CACHE[key].get(lang)
    if not keyboard_data:
        return None

    if isinstance(keyboard_data, str):
        keyboard_data = json.loads(keyboard_data)

    markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=btn["text"].format(**format_vars),
                url=btn.get("url").format(**format_vars) if btn.get("url") else None,
                callback_data=btn.get("callback").format(**format_vars) if btn.get("callback") else None
            )
            for btn in row
        ]
        for row in keyboard_data.get("inline_keyboard", [])
    ]
)
    return markup
