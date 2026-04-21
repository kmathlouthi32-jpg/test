import re
from config import get_spoofing_services

def remove_backslashes(s: str) -> str:
    return s.replace("\\", "")

def escape_markdown_text(text: str) -> str:
    escape_chars = r"[]()~`>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def escape_markdown_Ai_text(text: str) -> str:
    escape_chars = r"_[]()~>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def escape_markdown_user(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def is_name_valid(name: str):
    if name.upper() in get_spoofing_services():
        return 'Found'
    return bool(re.fullmatch(r'[A-Za-z\-]+', name))

def edit_text(text):
    lines = text.splitlines()
    title = lines[0][2:]
    full_script = lines[0][0]+"*"+lines[0][1:]+"*"+"\n\n"+lines[2][0]+"*"+lines[2][1:]+"*\n"+"_"+lines[3]+"_"+"\n\n"+lines[5][0]+"*"+lines[5][1:]+"*\n"+"_"+lines[6]+"_"+"\n\n"+lines[8][0]+"*"+lines[8][1:]+"*\n"+"_"+lines[9]+"_"+"\n\n"+lines[11][0]+"*"+lines[11][1:]+"*\n"+"_"+lines[12]+"_"
    return title, full_script
