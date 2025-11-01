from datetime import datetime
from .text_utils import escape_markdown

def duration(code: str):
    mapping = {
        '2HOUR': '2Hours',
        '1DAYZ': '1Day',
        '3DAYZ': '3Days',
        '1WEEK': '1Week',
        '1MNTH': '1Month'
    }
    return mapping.get(code)

def check_subscription(expiry_date):
    if expiry_date == 'N/A':
        return 'Null'
    now = datetime.now()
    expire_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
    return expire_date > now

def get_wallet_message(symbol: str, amount: float):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    symbol = symbol.upper()

    plans = {20: '1 Day Plan', 50: '4 Days Plan', 90: '1 Week Plan', 200: '1 Month Plan'}
    wallets = {
        'USDT': 'TRRVAuPEGJ4EgE33u1pV6gNUXxM1R5v1aY',
        'BTC': 'bc1q98y83fh28y6ysklu9qmla7enuegldmgdcdawvk',
        'ETH': '0xc76acc06684b2e2a2d43b9ba3b5f2618cd7a6307',
        'SOL': '8Ra9HKVrKNakEeQfqDzrVn1sFoQoFmbR51UHMRweT9hY',
        'LTC': 'LRJ8n55djedy4jyKP3Kkqi6iEy3BYC1FLt'
    }

    plan = plans.get(amount, "Unknown Plan")
    wallet = wallets.get(symbol, "N/A")

    return fr"""ℹ *Payment Details*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🪙 *Currency:* `{symbol}`
💰 *Amount:* `{amount-0.01}$`
📅 *Date:* `{escape_markdown(now)}`
⏳ *Plan:* `{plan}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💳 *Wallet:* `{wallet}`

🔐 *To complete your purchase:*
Send the amount via the *{symbol}* wallet and send a screenshot to Support\."""
