import phonenumbers
from phonenumbers import NumberParseException
from langcodes import get as get_lang
from config import get_country_language

def get_region_language(phone_number: str) -> str:
    try:
        parsed_number = phonenumbers.parse(phone_number)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        if not region_code:
            return "English (en)"

        lang_code = get_country_language(region_code)
        if not lang_code:
            return "English (en)"

        language_name = get_lang(lang_code).language_name()
        return f"{language_name} ({region_code.lower()})"

    except Exception:
        return "English (en)"


def is_valid_phone_number(number: str, region: str = None) -> bool:
    try:
        parsed_number = phonenumbers.parse(number, region)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False
    
