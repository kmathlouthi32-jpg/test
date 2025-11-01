# bot/languages.py
# Lazily load the country->language mapping to avoid heavy import-time memory usage.

_country_lang = None

def _load_mapping():
    # This function returns the full mapping. Only called once on-demand.
    return {
    "AD": "ca", "AE": "ar", "AF": "fa", "AG": "en", "AL": "sq", "AM": "hy", "AO": "pt", "AR": "es","AT": "de", "AU": "en", "AZ": "az", "BA": "bs", "BB": "en", "BD": "bn", "BE": "nl", "BF": "fr",
    "BG": "bg", "BH": "ar", "BI": "fr", "BJ": "fr", "BN": "ms", "BO": "es", "BR": "pt", "BS": "en","BT": "dz", "BW": "en", "BY": "be", "BZ": "en", "CA": "en", "CD": "fr", "CF": "fr", "CG": "fr",
    "CH": "de", "CI": "fr", "CL": "es", "CM": "fr", "CN": "zh", "CO": "es", "CR": "es", "CU": "es","CV": "pt", "CY": "el", "CZ": "cs", "DE": "de", "DJ": "fr", "DK": "da", "DM": "en", "DO": "es",
    "DZ": "ar", "EC": "es", "EE": "et", "EG": "ar", "ER": "ti", "ES": "es", "ET": "am", "FI": "fi","FJ": "en", "FM": "en", "FR": "fr", "GA": "fr", "GB": "en", "GD": "en", "GE": "ka", "GH": "en",
    "GM": "en", "GN": "fr", "GQ": "es", "GR": "el", "GT": "es", "GW": "pt", "GY": "en", "HN": "es","HR": "hr", "HT": "ht", "HU": "hu", "ID": "id", "IE": "en", "IL": "he", "IN": "hi", "IQ": "ar",
    "IR": "fa", "IS": "is", "IT": "it", "JM": "en", "JO": "ar", "JP": "ja", "KE": "en", "KG": "ky","KH": "km", "KI": "en", "KM": "ar", "KN": "en", "KP": "ko", "KR": "ko", "KW": "ar", "KZ": "kk",
    "LA": "lo", "LB": "ar", "LC": "en", "LI": "de", "LK": "si", "LR": "en", "LS": "en", "LT": "lt","LU": "lb", "LV": "lv", "LY": "ar", "MA": "ar", "MC": "fr", "MD": "ro", "ME": "sr", "MG": "mg",
    "MH": "en", "ML": "fr", "MM": "my", "MN": "mn", "MR": "ar", "MT": "mt", "MU": "en", "MV": "dv","MW": "en", "MX": "es", "MY": "ms", "MZ": "pt", "NA": "en", "NE": "fr", "NG": "en", "NI": "es",
    "NL": "nl", "NO": "no", "NP": "ne", "NZ": "en", "OM": "ar", "PA": "es", "PE": "es", "PG": "en","PH": "tl", "PK": "ur", "PL": "pl", "PT": "pt", "PW": "en", "PY": "es", "QA": "ar", "RO": "ro",
    "RS": "sr", "RU": "ru", "RW": "rw", "SA": "ar", "SB": "en", "SC": "fr", "SD": "ar", "SE": "sv","SG": "ms", "SI": "sl", "SK": "sk", "SL": "en", "SM": "it", "SN": "fr", "SO": "so", "SR": "nl",
    "SS": "en", "ST": "pt", "SV": "es", "SY": "ar", "SZ": "en", "TD": "fr", "TG": "fr", "TH": "th","TJ": "tg", "TL": "pt", "TM": "tk", "TN": "ar", "TO": "to", "TR": "tr", "TT": "en", "TV": "en",
    "TZ": "sw", "UA": "uk", "UG": "en", "US": "en", "UY": "es", "UZ": "uz", "VA": "la", "VC": "en","VE": "es", "VN": "vi", "VU": "bi", "WS": "sm", "YE": "ar", "ZA": "en", "ZM": "en", "ZW": "en",
}

def get_country_language(country_code: str, default: str = "en"):
    global _country_lang
    if _country_lang is None:
        _country_lang = _load_mapping()
    return _country_lang.get(country_code.upper(), default)

