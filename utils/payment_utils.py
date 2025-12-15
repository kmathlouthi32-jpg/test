from datetime import datetime
from .text_utils import escape_markdown
import httpx
from config import get_admin

COINS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ltc": "litecoin",
    "sol": "solana",
    "usdt": "tether"
}

def get_price(symbol):
    symbol = symbol.lower()
    if symbol not in COINS:
        raise ValueError(f"Unsupported coin: {symbol}")

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": COINS[symbol],
        "vs_currencies": "usd"
    }

    r = httpx.get(url, params=params)

    # validate response
    if r.status_code != 200:
        raise Exception(f"API error: {r.status_code} | {r.text}")

    data = r.json()

    # check if coin exists in response
    if COINS[symbol] not in data:
        raise Exception(f"CoinGecko returned no data: {data}")

    return data[COINS[symbol]]["usd"]


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

def get_wallet_message(symbol: str, amount: float, wallet_type: int):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    symbol = symbol.upper()

    plans = {15:'V.I.P Spoofer',20: '1 Day Plan', 50: '4 Days Plan', 90: '1 Week Plan', 200: '1 Month Plan', 1000: 'LifeTime Plan'}
    wallets = [{
        'USDT': 'TRRVAuPEGJ4EgE33u1pV6gNUXxM1R5v1aY',
        'BTC': '12g9D3pdhse6HSS38LYJr9bwXUGkeRbVHd',
        'ETH': '0xc76acc06684b2e2a2d43b9ba3b5f2618cd7a6307',
        'SOL': '8Ra9HKVrKNakEeQfqDzrVn1sFoQoFmbR51UHMRweT9hY',
        'LTC': 'LRJ8n55djedy4jyKP3Kkqi6iEy3BYC1FLt'
    },
    {
        'USDT': 'THqWBtVxYRpWhgmMNd2M5nMkjTTVmsVgxh',
        'BTC': '1M6Q4pFzofeBvA9e2CQ9rhtLyLkLc34p3q',
        'ETH': '0x1c89c55def70cb0fccaf058abfc5a1e493d0e297',
        'SOL': '5bPVRzUqc4ThfNST9uaKMn8PoS3xip1JxRShb8PWwWFW',
        'LTC': 'LMWe7aWQkBcQZT5fzhfPDvZMHdYg9rwuwp'
    }
    ]

    plan = plans.get(amount, "Unknown Plan")
    wallet = wallets[wallet_type].get(symbol, "N/A")

    return fr"""ℹ *Payment Details*
━━━━━━━━━━━━━━━
🪙 *Currency:* {symbol}
💰 *Amount:* {escape_markdown(usd_to_crypto(symbol, amount))}
📅 *Date:* {escape_markdown(now)}
⏳ *Plan:* {escape_markdown(plan)}
💳 *Wallet:* `{wallet}`

🔐 *To complete your purchase:*
_Send the amount via the *{symbol}* wallet and send a screenshot to *[Support]({get_admin()['link']})*_\."""

