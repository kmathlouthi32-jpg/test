import re
import dns.resolver
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import httpx

async def get_ip_info(ip: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"http://ip-api.com/json/{ip}",
                params={"fields": "status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting"}
            )
            data = r.json()
    except Exception as e:
        return {"error": str(e)}

    if data.get("status") != "success":
        return {"error": data.get("message", "Lookup failed")}

    return {
        "ip": ip,
        "country": f"{data['country']} ({data['countryCode']})",
        "region": data["regionName"],
        "city": data["city"],
        "zip": data["zip"],
        "timezone": data["timezone"],
        "coords": f"{data['lat']}, {data['lon']}",
        "isp": data["isp"],
        "org": data["org"],
        "asn": data["as"],
        "proxy_vpn": data["proxy"],
        "hosting": data["hosting"],
    }

PROVIDER_MAP = {
    "gmail.com": "Google Gmail",
    "yahoo.com": "Yahoo Mail",
    "outlook.com": "Microsoft Outlook",
    "hotmail.com": "Microsoft Hotmail",
    "icloud.com": "Apple iCloud",
    "protonmail.com": "ProtonMail",
    "zoho.com": "Zoho Mail",
}

DISPOSABLE_DOMAINS = {
    "tempmail.com", "throwaway.email", "guerrillamail.com",
    "mailinator.com", "yopmail.com", "trashmail.com",
}


def get_phone_info(phone: str) -> dict:
    try:
        parsed = phonenumbers.parse(phone, "TN")  # "TN" as fallback if no country code
    except Exception as e:
        return {"error": str(e)}

    is_valid = phonenumbers.is_valid_number(parsed)
    is_possible = phonenumbers.is_possible_number(parsed)
    number_type = phonenumbers.number_type(parsed)

    # fixed: use the dict directly instead of _VALUES_TO_NAMES
    type_map = {
        0: "Fixed line",
        1: "Mobile",
        2: "Fixed or mobile",
        3: "Toll free",
        4: "Premium rate",
        5: "Shared cost",
        6: "VOIP",
        7: "Personal number",
        8: "Pager",
        9: "UAN",
        10: "Voicemail",
        99: "Unknown",
    }

    return {
        "number": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
        "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
        "country_code": f"+{parsed.country_code}",
        "national_number": str(parsed.national_number),
        "valid": is_valid,
        "possible": is_possible,
        "type": type_map.get(number_type, "Unknown"),
        "carrier": carrier.name_for_number(parsed, "en"),
        "location": geocoder.description_for_number(parsed, "en"),
        "region": phonenumbers.region_code_for_number(parsed),
        "timezones": list(timezone.time_zones_for_number(parsed)),
    }

def get_email_info(email: str) -> dict:
    # format check
    pattern = r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$'
    format_valid = bool(re.match(pattern, email))

    if not format_valid:
        return {"error": "Invalid email format"}

    local, domain = email.split("@", 1)

    # MX records
    mx_records = []
    mx_found = False
    try:
        answers = dns.resolver.resolve(domain, "MX")
        mx_found = True
        mx_records = sorted(
            [str(r.exchange).rstrip(".") for r in answers],
            key=lambda x: x
        )
    except Exception:
        pass

    # A record
    a_found = False
    ip_addresses = []
    try:
        a_answers = dns.resolver.resolve(domain, "A")
        a_found = True
        ip_addresses = [str(r) for r in a_answers]
    except Exception:
        pass

    # score
    score = 0
    if format_valid: score += 40
    if mx_found:     score += 40
    if a_found:      score += 20

    filled = int(score / 10)
    bar = "█" * filled + "░" * (10 - filled)

    return {
        "email": email,
        "local": local,
        "domain": domain,
        "format_valid": format_valid,
        "mx_found": mx_found,
        "a_found": a_found,
        "provider": PROVIDER_MAP.get(domain, domain),
        "disposable": domain in DISPOSABLE_DOMAINS,
        "mx_records": mx_records,
        "ip_addresses": ip_addresses,
        "score": score,
        "score_bar": f"[{bar}]",
    }
