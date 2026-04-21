import phonenumbers
from phonenumbers import NumberParseException

def is_valid_phone_number(number: str, region: str = None) -> bool:
    try:
        parsed_number = phonenumbers.parse(number, region)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False

def mask_phone_number(number: str) -> str:

    if not number or not number.startswith('+'):
        return number

    prefix = number[:3]   # '+' + first 3 digits
    suffix = number[-3:]  # last 2 digits
    masked = '*' * (len(number) - len(prefix) - len(suffix))

    return f"{prefix}{masked}{suffix}"
