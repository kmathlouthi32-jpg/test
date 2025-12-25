import re
from config import get_spoofing_services

def escape_markdown_link(text: str) -> str:
    escape_chars = r"*~`>#+-=|.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def escape_markdown_text(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def escape_markdown_user(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def escape_markdown(text: str) -> str:
    escape_chars = r"*[]()~`>#+-=|.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def is_name_valid(name: str):
    if name.upper() in get_spoofing_services():
        return 'Found'
    return bool(re.fullmatch(r'[A-Za-z\-]+', name))
