from typing import Dict
import re
from .database import db
from utils.translate import fast_translate
from utils.text_utils import escape_markdown, escape_markdown_link
import asyncio

# =============================
# CONSTANTS
# =============================

COMMAND_PATTERN = re.compile(r"/[a-zA-Z0-9_]+")

FORMAT_TOKENS = {
    "{bold}": "__FMT_BOLD_OPEN__",
    "{/bold}": "__FMT_BOLD_CLOSE__",
    "{italic}": "__FMT_ITALIC_OPEN__",
    "{/italic}": "__FMT_ITALIC_CLOSE__",
    "{code}": "__FMT_CODE_OPEN__",
    "{/code}": "__FMT_CODE_CLOSE__",
    "{br}": "__FMT_BR__",
}

FORMAT_RESTORE = {
    "__FMT_BOLD_OPEN__": "*",
    "__FMT_BOLD_CLOSE__": "*",
    "__FMT_ITALIC_OPEN__": "_",
    "__FMT_ITALIC_CLOSE__": "_",
    "__FMT_CODE_OPEN__": "`",
    "__FMT_CODE_CLOSE__": "`",
    "__FMT_BR__": "\n",
}


# =============================
# PROTECT / RESTORE HELPERS
# =============================

def protect_formatting(text: str) -> str:
    for k, v in FORMAT_TOKENS.items():
        text = text.replace(k, v)
    return text


def restore_formatting(text: str) -> str:
    for k, v in FORMAT_RESTORE.items():
        text = text.replace(k, v)
    return text


def protect_commands(text: str):
    commands = {}

    def repl(match):
        key = f"__CMD_{len(commands)}__"
        commands[key] = match.group(0)
        return key

    return COMMAND_PATTERN.sub(repl, text), commands


def restore_commands(text: str, commands: dict):
    for k, v in commands.items():
        text = text.replace(k, v)
    return text


def protect_variables(text: str):
    variables = {}
    i = 0

    def repl(match):
        nonlocal i
        key = f"__VAR_{i}__"
        variables[key] = match.group(0)
        i += 1
        return key

    protected = re.sub(r"\{[a-zA-Z0-9_]+\}", repl, text)
    return protected, variables


def restore_variables(text: str, variables: dict):
    for k, v in variables.items():
        text = text.replace(k, v)
    return text

def restore_formatting_tokens(text: str) -> str:
    return (
        text
        .replace("__FMT_BOLD_OPEN__", "{bold}")
        .replace("__FMT_BOLD_CLOSE__", "{/bold}")
        .replace("__FMT_ITALIC_OPEN__", "{italic}")
        .replace("__FMT_ITALIC_CLOSE__", "{/italic}")
        .replace("__FMT_CODE_OPEN__", "{code}")
        .replace("__FMT_CODE_CLOSE__", "{/code}")
        .replace("__FMT_BR__", "{br}")
    )

def tokens_to_markdown(text: str) -> str:
    return (
        text
        .replace("{bold}", "*")
        .replace("{/bold}", "*")
        .replace("{italic}", "_")
        .replace("{/italic}", "_")
        .replace("{code}", "`")
        .replace("{/code}", "`")
        .replace("{br}", "\n")
    )


# =============================
# CACHE
# =============================

MESSAGE_CACHE: Dict[str, Dict[str, str]] = {}


# =============================
# LOAD MESSAGES
# =============================

async def load_messages():
    global MESSAGE_CACHE
    MESSAGE_CACHE = await db.load_all_messages() or {}
    print(f"🚀 Loaded {len(MESSAGE_CACHE)} messages into memory")


def is_lang_exist(lang: str) -> bool:
    return lang in MESSAGE_CACHE.get("start_message", {})


SEM = asyncio.Semaphore(5)  # tune: 3–10 depending on API limits

async def translate_one(key, data, lang):
    async with SEM:
        base = data.get("en")
        if not base or lang in data:
            return

        # protect
        text = protect_formatting(base)
        text, variables = protect_variables(text)
        text, commands = protect_commands(text)

        # translate
        text = await fast_translate(text, lang)

        # restore
        text = restore_commands(text, commands)
        text = restore_variables(text, variables)
        text = restore_formatting_tokens(text)

        await db.set_message(key, lang, text)
        MESSAGE_CACHE[key][lang] = text


async def preload_language(lang: str):
    print(f"🌍 Preloading language: {lang}")

    tasks = [
        translate_one(key, data, lang)
        for key, data in MESSAGE_CACHE.items()
    ]

    await asyncio.gather(*tasks)

    print(f"✅ Language '{lang}' ready")


# =============================
# GET MESSAGE
# =============================

def get_message(key: str, lang: str = "en") -> str:
    data = MESSAGE_CACHE.get(key)
    if not data:
        raise KeyError(f"Message '{key}' not found")

    return data.get(lang) or data.get("en")


# =============================
# RENDER MESSAGE (FINAL STEP)
# =============================

def render_message(key: str, lang: str = "en", **kwargs) -> str:
    text = get_message(key, lang)

    # 1️⃣ Protect formatting tokens so .format() doesn't break
    text = (
        text
        .replace("{bold}", "__FMT_BOLD_OPEN__")
        .replace("{/bold}", "__FMT_BOLD_CLOSE__")
        .replace("{italic}", "__FMT_ITALIC_OPEN__")
        .replace("{/italic}", "__FMT_ITALIC_CLOSE__")
        .replace("{code}", "__FMT_CODE_OPEN__")
        .replace("{/code}", "__FMT_CODE_CLOSE__")
        .replace("{br}", "__FMT_BR__")
    )

    # 2️⃣ Replace variables
    text = text.format(**kwargs)
    if key != 'wallet_message':
        text = escape_markdown(text)
    else:
        text = escape_markdown_link(text)

    # 3️⃣ Restore Markdown symbols
    text = (
        text
        .replace("__FMT_BOLD_OPEN__", "*")
        .replace("__FMT_BOLD_CLOSE__", "*")
        .replace("__FMT_ITALIC_OPEN__", "_")
        .replace("__FMT_ITALIC_CLOSE__", "_")
        .replace("__FMT_CODE_OPEN__", "`")
        .replace("__FMT_CODE_CLOSE__", "`")
        .replace("__FMT_BR__", "\n")
    )

    # 4️⃣ Escape for MarkdownV2
    return text




# =============================
# HOT RELOAD
# =============================

async def reload_messages():
    await load_messages()
