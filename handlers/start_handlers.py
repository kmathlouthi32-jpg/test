from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot
from utils import get_user_info, user_exists, add_user, get_user_count, escape_markdown
from config import get_admin, get_groups, get_video

def start_message(name):
    return fr"""🐉 *Welcome* `{name}`\!

🔥 *DRAGON OTP BOT* — The Ultimate *Spoofing* Experience

*DRAGON OTP* is the \#1 Telegram\-based OTP system built for professionals\.  
Powered by *cutting\-edge AI* 🤖, 🌍 *global voice routing*, and ⚡ *real\-time control* — it delivers unmatched *speed*, *stealth*, and *precision*\.

Whether you're testing, *analyzing*, or *automating* — *DRAGON OTP* gives you the *tools* to *dominate* with *confidence*\. 💪"""

def admin_start_message(name):
    return fr"""🔥 Welcome back, {name}\!

👑 You’re logged in as the Owner of *DRAGON OTP BOT*\.  
Manage users, keys, and sales — your control center awaits ⚙️
"""

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔥 Buy Now", callback_data="purchase")
        ],
        [
            InlineKeyboardButton(text="👤 My Account", callback_data='plan'),
            InlineKeyboardButton(text="⚙️ Commands", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="🌐 Community", url=get_groups()['main_channel_link']),
            InlineKeyboardButton(text="✅ Vouches", url=get_groups()['vouches_LINK'])
        ],
        [
            
            InlineKeyboardButton(text="💬 Support / Contact", url=get_admin()['link'])
        ]
    ])

def admin_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔑 Keys", callback_data='keys'),
            InlineKeyboardButton(text="⚙️ Commands", callback_data="help")
        ],
        [
            
            InlineKeyboardButton(text="🔑 generate keys", callback_data='g_keys')
        ]
    ])

async def start_command(message: Message, bot:Bot):
    user_id = message.from_user.id
    if not(await get_user_info(user_id,'banned')):
        name = message.from_user.first_name
        if await user_exists(user_id)==False:
            await add_user(user_id)
            if message.from_user.username:
                username = "@"+message.from_user.username
            else:
                username = 'N/A'
            await bot.send_message(chat_id=get_groups()['new_users_ID'],text=fr'''🆕 *New user*: {await get_user_count()}
*Username*\: {escape_markdown(username)}
*Name*\: `{escape_markdown(name)}`
*User ID*\: `{str(user_id)}`''',parse_mode='MarkdownV2')
        if user_id == get_admin()['id']:
            await message.answer(admin_start_message(name), reply_markup=admin_start_keyboard(),parse_mode='MarkdownV2')
            return
        await message.answer_video(get_video(),caption=start_message(name), reply_markup=start_keyboard(),parse_mode='MarkdownV2')

async def start_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    if not(await get_user_info(user_id,'banned')):
        name = callback.from_user.first_name
        if callback.data == 'back1':
            await callback.message.delete()
        else:
            for i in range(6):
                await bot.delete_message(user_id,callback.message.message_id-i)
        if user_id == get_admin()['id']:
            await callback.message.answer(admin_start_message(name), reply_markup=admin_start_keyboard(),parse_mode='MarkdownV2')
            return
        await callback.message.answer_video(get_video(),caption=start_message(name), reply_markup=start_keyboard(),parse_mode='MarkdownV2')

async def unknown_command(message: Message):
    user_id = message.from_user.id
    if not(await get_user_info(user_id,'banned')):
        await message.answer("❌ Unknown command.")

async def help_command(message: Message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned'): return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])
    await message.answer(r"""*CROWS OTP — Commands Panel*
    
❓ *Core Commands*
• `/redeem` — Redeem your access key  
• `/phonelist` — View spoof\-ready numbers  
• `/plan` — Check your account status  
• `/purchase` — Buy access or upgrade  
• `/help` — Show this command list

⚙️ *OTP Modules*
• `/call` — Universal OTP call \(any service\)  
• `/paypal` — PayPal OTP  
• `/venmo` — Venmo OTP  
• `/applepay` — Apple Pay OTP  
• `/coinbase` — Coinbase OTP  
• `/microsoft` — Microsoft OTP  
• `/amazon` — Amazon OTP  
• `/quadpay` — Quadpay OTP  
• `/cashapp` — Cash App OTP  
• `/citizens` — Citizens Bank OTP  
• `/marcus` — Marcus OTP  
• `/creditcard` — Credit Card OTP  
• `/carrier` — Carrier Verification OTP
• `/repcall` — Call Company
                         
👤 *Custom Features*
• `/setscript` — Create a custom script  
• `/script` — View your current script  
• `/scriptcall` — Launch a custom call  
• `/setvoice` — Select a voice for spoofing  
• `/voicelist` — View available voices  
• `/recall` — Repeat the last victim call
""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def help_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned'): return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])
    await callback.message.delete()
    await callback.message.answer(r"""*CROWS OTP — Commands Panel*
    
❓ *Core Commands*
• `/redeem` — Redeem your access key  
• `/phonelist` — View spoof\-ready numbers  
• `/plan` — Check your account status  
• `/purchase` — Buy access or upgrade  
• `/help` — Show this command list

⚙️ *OTP Modules*
• `/call` — Universal OTP call \(any service\)  
• `/paypal` — PayPal OTP  
• `/venmo` — Venmo OTP  
• `/applepay` — Apple Pay OTP  
• `/coinbase` — Coinbase OTP  
• `/microsoft` — Microsoft OTP  
• `/amazon` — Amazon OTP  
• `/quadpay` — Quadpay OTP  
• `/cashapp` — Cash App OTP  
• `/citizens` — Citizens Bank OTP  
• `/marcus` — Marcus OTP  
• `/creditcard` — Credit Card OTP  
• `/carrier` — Carrier Verification OTP
• `/repcall` — Call Company
                                  
👤 *Custom Features*
• `/setscript` — Create a custom script  
• `/script` — View your current script  
• `/scriptcall` — Launch a custom call  
• `/setvoice` — Select a voice for spoofing  
• `/voicelist` — View available voices  
• `/recall` — Repeat the last victim call
""", reply_markup=keyboard, parse_mode='MarkdownV2')
