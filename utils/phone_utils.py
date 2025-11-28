import phonenumbers
from phonenumbers import NumberParseException,geocoder


def get_region_language(phone_number: str) -> str:
    if phone_number[0] != '+':
        phone_number = '+'+phone_number
    try:
        parsed_number = phonenumbers.parse(phone_number)

        country_name = geocoder.country_name_for_number(parsed_number, "en")

        return country_name or "Unknown"
    except Exception:
        return "Unknown"


def is_valid_phone_number(number: str, region: str = None) -> bool:
    if number[0] != '+':
        number = '+'+number
    try:
        parsed_number = phonenumbers.parse(number, region)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False
    
