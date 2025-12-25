import asyncio
from googletrans import Translator
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from utils import escape_markdown

translator = Translator()

def protect_commands(text: str):
    command_map = {}
    counter = 0

    def replacer(match):
        nonlocal counter
        key = f"__CMD_{counter}__"
        command_map[key] = match.group(0)
        counter += 1
        return key

    protected_text = re.sub(r'/[a-zA-Z0-9_]+', replacer, text)
    return protected_text, command_map

def restore_commands(text: str, command_map: dict):
    for key, value in command_map.items():
        text = text.replace(key, value)
    return text

async def fast_translate(text: str, dest: str, retries=3):
    for attempt in range(retries):
        try:
            return await asyncio.to_thread(
                lambda: translator.translate(text, dest=dest).text
            )
        except Exception as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(1)

async def translate_preserve_commands(text: str, dest: str = "en"):
    protected, command_map = protect_commands(text)

    translated = await fast_translate(protected, dest)

    restored = restore_commands(translated, command_map)

    return restored

async def translate_button_text(markup: InlineKeyboardMarkup, dest="fr") -> InlineKeyboardMarkup:
    button_texts = [btn.text for row in markup.inline_keyboard for btn in row]

    # Combine with a special separator unlikely to appear in text
    combined_text = "||SEP||".join(button_texts)

    # Translate once
    translated_combined = await fast_translate(combined_text, dest)

    # Split back
    translated_texts = translated_combined.split("||SEP||")

    # Rebuild keyboard
    new_keyboard = []
    idx = 0
    for row in markup.inline_keyboard:
        new_row = []
        for btn in row:
            new_btn = InlineKeyboardButton(
                text=translated_texts[idx],
                callback_data=btn.callback_data,
                url=btn.url
            )
            idx += 1
            new_row.append(new_btn)
        new_keyboard.append(new_row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=new_keyboard)
    return keyboard


    # ---- MESSAGE ----
    protected_text, cmd_map = protect_commands(message_text)

    if lang != "en":
        translated_text = await fast_translate(protected_text, lang)
        translated_text = restore_commands(translated_text, cmd_map)
    else:
        translated_text = message_text

    # ---- BUTTONS ----
    if lang != "en":
        # Create placeholders
        btn_map = {}
        lines = []
        idx = 0

        for row in keyboard.inline_keyboard:
            for btn in row:
                key = f"__BTN_{idx}__"
                btn_map[key] = btn.text
                lines.append(f"{key}: {btn.text}")
                idx += 1

        # Translate ONCE
        translated_block= await fast_translate("\n".join(lines), lang)

        # Extract translations
        translated_btns = {}
        for line in translated_block.splitlines():
            m = re.match(r'(__BTN_\d+__):\s*(.+)', line)
            if m:
                translated_btns[m.group(1)] = m.group(2)

        # Rebuild keyboard
        new_keyboard = []
        idx = 0
        for row in keyboard.inline_keyboard:
            new_row = []
            for btn in row:
                key = f"__BTN_{idx}__"
                new_row.append(
                    InlineKeyboardButton(
                        text=translated_btns.get(key, btn.text),  # safe fallback
                        callback_data=btn.callback_data,
                        url=btn.url
                    )
                )
                idx += 1
            new_keyboard.append(new_row)

        keyboard = InlineKeyboardMarkup(inline_keyboard=new_keyboard)

    # ---- MARKDOWN ----
    safe_text = escape_markdown(translated_text)

    return safe_text, keyboard

