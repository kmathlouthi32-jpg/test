from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from utils import get_user_info, escape_markdown, check_subscription, redeem_key, get_wallet_message
from config import get_admin, get_groups
from datetime import datetime
from aiogram import Bot

def subscription_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Plans", callback_data="purchase"),
         InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])]
    ])

def pricing_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💫 1 Day — $19.99", callback_data="20"),
            InlineKeyboardButton(text="🔥 4 Days — $49.99", callback_data="50"),
        ],
        [
            InlineKeyboardButton(text="💎 1 Week — $89.99", callback_data="90"),
            InlineKeyboardButton(text="🚀 1 Month — $199.99", callback_data="200"),
        ],
        [
            InlineKeyboardButton(text="🔙 Back To menu", callback_data="back1")
        ]
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
    return r"""💰 Choose your subscription plan

🔹 *1 Day* Access — *$19\.99*
🔹 *4 Days* Access — *$49\.99*
🔹 *1 Week* Access — *$89\.99*
🔹 *1 Month* Access — *$199\.99*

Select the plan that suits you 👇"""

def subscirber_profile_message(username, user_id, date, days_left):
    return fr"""*🐉 DRAGON OTP — User Dashboard*

👤 *Username*: `{escape_markdown(username)}`
🆔 *User ID*: `{user_id}`

💠 *Plan*: `Premium`
🟢 *Status*: `Active`

📅 *Start Date*: `{escape_markdown(date)}`
🕒 *Days Remaining*: `{escape_markdown(days_left)}`

⚡ *Features*:  
\- Unlimited OTP Access ✅  
\- Real\-time Spoofing Controls ⚡  
\- Priority Support 💬"""

def subscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])

def unsubscirber_profile_message(username, user_id):
    return fr"""*🐉 DRAGON OTP — User Dashboard*

👤 *Username*: `{escape_markdown(username)}`
🆔 *User ID*: `{user_id}`

💠 *Plan*: `Basic`
🔴 *Status*: `Not Active`

⚡️ *Features \(Upgrade to Unlock\)*:
\- Limited OTP Access 🚫
\- Spoof Controls Locked 🔒
\- Standard Support 🕓"""

def unsubscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Buy Now", callback_data="purchase")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])

async def purchase_command(message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    await message.answer(pricing_message(), reply_markup=pricing_keyboard(), parse_mode='MarkdownV2')

async def purchase_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    await callback.message.delete()
    await callback.message.answer(pricing_message(), reply_markup=pricing_keyboard(), parse_mode='MarkdownV2')

async def wallets_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    price = callback.data
    await callback.message.delete()
    await callback.message.answer(r'''💸 Pick a *wallet* to continue\.
💬 Other options available via *Support*\.''', reply_markup=wallets_keyboard(price), parse_mode='MarkdownV2')

async def my_profile_command(message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    if message.from_user.username:
        username = message.from_user.username
    else:
        username = 'N/A'
    if check_subscription(await get_user_info(user_id, 'expiry_date')) == True:
        expiry_date = await get_user_info(user_id, 'expiry_date')
        date = expiry_date[0:16]
        expiry_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
        days_left = str(expiry_date-datetime.now())
        days_left = days_left[:days_left.find(',')]
        await message.answer(subscirber_profile_message(username, user_id, date, days_left), reply_markup=subscriber_keyboard(), parse_mode='MarkdownV2')
        return
    await message.answer(unsubscirber_profile_message(username, user_id), reply_markup=unsubscriber_keyboard(), parse_mode='MarkdownV2')

async def my_profile_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    if callback.message.from_user.username:
        username = callback.message.from_user.username
    else:
        username = 'N/A'
    if check_subscription(await get_user_info(user_id, 'expiry_date')) == True:
        expiry_date = await get_user_info(user_id, 'expiry_date')
        date = expiry_date[0:16]
        expiry_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
        days_left = str(expiry_date-datetime.now())
        days_left = days_left[:days_left.find(',')]
        await callback.message.delete()
        await callback.message.answer(subscirber_profile_message(username, user_id, date, days_left), reply_markup=subscriber_keyboard(), parse_mode='MarkdownV2')
        return
    await callback.message.delete()
    await callback.message.answer(unsubscirber_profile_message(username, user_id), reply_markup=unsubscriber_keyboard(), parse_mode='MarkdownV2')

async def redeem_keys(message,bot:Bot):
    user_id = message.from_user.id
    if await get_user_info(user_id, 'banned'): return
    parts = message.text.split()
    if len(parts)<2:
        await message.answer("❌ No Activation Key\nUse /redeem <key> to activate your access.")
        return
    msg = await redeem_key(user_id, parts[1])
    await message.answer(msg)
    duration_text = msg[2:msg.find('K')-1]
    if message.from_user.username:
        username = "@"+message.from_user.username
    else:
        username = 'N/A'
    name = message.from_user.first_name
    await bot.send_message(chat_id=get_groups()['redeemed_keys_ID'],text=fr'''*Key For {duration_text}*
Redeemed by {escape_markdown(username)}
Name: `{escape_markdown(name)}`
Chat Id: `{user_id}`
Key: `{parts[1]}`''',parse_mode='MarkdownV2')

async def wallet_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    price_symbol = callback.data
    amount = price_symbol[:price_symbol.find(':')]
    symbol = price_symbol[price_symbol.find(':')+1:]
    await callback.message.delete()
    await callback.message.answer(get_wallet_message(symbol,float(amount)), reply_markup=subscription_keyboard(), parse_mode='MarkdownV2')