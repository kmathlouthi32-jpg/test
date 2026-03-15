from datetime import datetime
import httpx
from config import get_admin
from .messages_manager import render_message

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

def get_wallet_message(symbol: str, amount: float, wallet_type: int, lang:str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    symbol = symbol.upper()

    plans = {15:'V.I.P Spoofer',25: '1 Day Plan', 89: '4 Days Plan', 149: '1 Week Plan', 299: '1 Month Plan', 999: 'LifeTime Plan'}
    wallets = [{
        'USDT': 'TY4Eh8RPdrhWSokWq9j9S4zVw7gd1Vrbaf',
        'BTC': '1KhvoitTrnopPqhxR1ayZ2ERw3d1g5BfdC',
        'ETH': '0x91ab56856eff7bc410fdac41c35a75d4e83410f6',
        'SOL': 'GEPAmKTxPpM3mxYGze9CXmnSxAtZu1xQ9L9v7GEqmFts',
        'LTC': 'LNFkiNNuqjLtY1vN4r3ihegnYfKmsc75Nm'
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
    amnt = usd_to_crypto(symbol, amount)
    #now = escape_markdown(now)
    #plan = escape_markdown(plan)
    message = render_message('wallet_message',lang,symbol=symbol,amount=amnt,date=now,plan=plan,wallet=wallet,link=get_admin()['link'])
    return message


