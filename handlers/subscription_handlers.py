from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from utils import escape_markdown, check_subscription, get_wallet_message, db, get_user_cached, update_user_cache
from config import get_admin, get_groups
from datetime import datetime
from aiogram import Bot

def pricing_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 V.I.P Spoofer — $14.99", callback_data="15")],
        [InlineKeyboardButton(text="💫 1 Day — $19.99", callback_data="20")],
        [InlineKeyboardButton(text="🔥 4 Days — $49.99", callback_data="50")],
        [InlineKeyboardButton(text="💎 1 Week — $89.99", callback_data="90")],
        [InlineKeyboardButton(text="🚀 1 Month — $199.99", callback_data="200")],
        [InlineKeyboardButton(text="♾️ LifeTime — $999.99", callback_data="1000")],
        [InlineKeyboardButton(text="🔙 Back To menu", callback_data="back1")]
    ])

def wallets_keyboard(price):
    return InlineKeyboardMarkup(
    inline_keyboard=[
        # Support row
        [
            InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])
        ],
        # Row: Major cryptos
        [
            InlineKeyboardButton(text="₿ BTC", callback_data=price+":btc"),
            InlineKeyboardButton(text="💲 USDT", callback_data=price+':usdt')
        ],
        # Row: Altcoins
        [
            InlineKeyboardButton(text="♢ ETH", callback_data=price+':eth'),
            InlineKeyboardButton(text="𝑳 LTC", callback_data=price+':ltc'),
            InlineKeyboardButton(text="◎ SOL", callback_data=price+':sol')
        ],
        # Navigation / back row
        [
            InlineKeyboardButton(text="🔙 Back", callback_data='purchase')
        ]
    ]
)

def pricing_message():
    return r"""💰 *Choose Your Subscription Package*:

Pick the package that fits your needs 👇"""

def subscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])

def unsubscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Purchase", callback_data="purchase")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])

def prices_message():
    return r"""💵 *Purchase USA With Spoofing*  💵

📅 *Pricing*:
 • 1 Day: $25 💲
 • 4 Days: $60 💲
 • 1 Week: $120 💲
 • 1 Month: $300 💲
 • Lifetime: $1500 💲
—————————————————————
💵 *Purchase Plans USA With Spoof \+ Europe With Spoofing* 💵

📅 *Pricing*:
• 1 Day: $30 💲
• 4 Days: $80 💲
• 1 Week: $150 💲
 • 1 Month: $450 💲
 • Lifetime: $2000 💲
—————————————————————"""

async def purchase_command(message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned'] == True: return
    await message.answer(pricing_message(), reply_markup=pricing_keyboard(), parse_mode='MarkdownV2')

async def purchase_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned'] == True: return
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(pricing_message(), reply_markup=pricing_keyboard(), parse_mode='MarkdownV2')

async def wallets_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned'] == True: return
    price = callback.data
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(r'''💸 Pick a *wallet* to continue\.
💬 Other options available via *Support*\.''', reply_markup=wallets_keyboard(price), parse_mode='MarkdownV2')

async def my_profile_command(message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned'] == True: return
    if check_subscription(user_data['expiry_date']) == True:
        expiry_date = user_data['expiry_date']
        expiry_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
        days_left = str(expiry_date-datetime.now())
        days_left = days_left[:days_left.find(',')]
        await message.answer(f'🕐 your Subscription Ends Within *{escape_markdown(days_left)}*', reply_markup=subscriber_keyboard(),parse_mode='MarkdownV2')
        return
    await message.answer('No Subscriptions Found ❌', reply_markup=unsubscriber_keyboard())

async def redeem_keys(message,bot:Bot):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    parts = message.text.split()
    if len(parts)<2:
        await message.answer("❌ No Activation Key\nUse /redeem <key> to activate your access.")
        return
    msg,duration_text,expiry = await db.redeem_key(user_id, parts[1], user_data['expiry_date'], user_data['rep'])
    await message.answer(msg)
    if duration_text == None:return
    if message.from_user.username:
        username = "@"+message.from_user.username
    else:
        username = 'N/A'
    name = message.from_user.first_name
    await update_user_cache(user_id, 'expiry_date', str(expiry))
    await bot.send_message(chat_id=get_groups()['redeemed_keys_ID'],text=fr'''*Key For {duration_text}*
Redeemed by {escape_markdown(username)}
Name: `{escape_markdown(name)}`
Chat Id: `{user_id}`
Key: `{parts[1]}`''',parse_mode='MarkdownV2')

async def wallet_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned'] == True: return
    price_symbol = callback.data
    amount = price_symbol[:price_symbol.find(':')]
    symbol = price_symbol[price_symbol.find(':')+1:]
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(get_wallet_message(symbol,float(amount),user_data['wallet']), parse_mode='MarkdownV2',disable_web_page_preview=True)

async def prices_command(message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned'] == True: return
    await message.answer(prices_message(), reply_markup=unsubscriber_keyboard(), parse_mode='MarkdownV2')



