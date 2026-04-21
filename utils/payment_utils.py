from datetime import datetime
import httpx
from config import get_admin
from typing import Union

COINS = {
    # your original stack
    "btc":  "bitcoin",
    "eth":  "ethereum",
    "ltc":  "litecoin",
    "sol":  "solana",
    "usdt": "tether",
    # stablecoins
    "usdc": "usd-coin",
    "dai":  "dai",
    # evm / l2
    "bnb":  "binancecoin",
    "pol":  "matic-network",
    "avax": "avalanche-2",
    "ton":  "the-open-network",
    "trx":  "tron",
    # other chains
    "xrp":  "ripple",
    "ada":  "cardano",
    "dot":  "polkadot",
    # meme
    "doge": "dogecoin",
    "shib": "shiba-inu",
}

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


def get_price(symbol: str, vs: str = "usd") -> Union[float, None]:
    symbol = symbol.lower().strip()

    if symbol not in COINS:
        supported = ", ".join(COINS.keys())
        raise ValueError(
            f"Unsupported coin: '{symbol}'. Supported: {supported}"
        )

    coin_id = COINS[symbol]
    url = f"{COINGECKO_BASE}/simple/price"
    params = {"ids": coin_id, "vs_currencies": vs}

    try:
        r = httpx.get(url, params=params, timeout=10)
        r.raise_for_status()
    except httpx.TimeoutException:
        raise Exception("CoinGecko request timed out")
    except httpx.HTTPStatusError as e:
        raise Exception(f"API error {e.response.status_code}: {e.response.text}")

    data = r.json()

    if coin_id not in data or vs not in data[coin_id]:
        raise Exception(f"No price data returned for {symbol.upper()}/{vs.upper()}")

    return data[coin_id][vs]


def usd_to_crypto(symbol, usd_amount):
    price = get_price(symbol)
    price = str(usd_amount/price)
    return f"{usd_amount}$ = {price[:10]} {symbol.upper()}"



def duration(code: str):
    mapping = {
        '2HOUR': '2Hours',
        '1DAYZ': '1Day',
        '3DAYZ': '3Days',
        '1WEEK': '1Week',
        '1MNTH': '1Month',
        'LIFE': 'Life'
    }
    return mapping.get(code)

def check_subscription(expiry_date):
    if expiry_date == 'N/A':
        return 'Null'
    now = datetime.now()
    expire_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
    return expire_date > now



