from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot
from utils import escape_markdown, check_subscription, get_user_cached, is_new_user
from config import get_admin, get_groups, get_video, spoof_message

def start_message(name):
    return fr"""👋 *Welcome {name} to DRAGON OTP BOT \- Ultimate Spoofing Experience* 🐉

*DRAGON OTP* is the \#1 Telegram\-based OTP spoofing system built for professionals\.

It combines cutting\-edge AI, global voice routing, and real\-time control to deliver the most advanced OTP grabbing experience on the market\.

Whether you're testing, analyzing, or automating — DRAGON OTP gives you the tools to dominate with speed, stealth, and precision\."""

def admin_start_message(name):
    return fr"""🔥 Welcome back, {name}\!

👑 You’re logged in as the Owner of *DRAGON OTP BOT*\.  
Manage users, keys, and sales — your control center awaits ⚙️
"""

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎯 Enter Bot", callback_data="enter")
        ],
        [
            InlineKeyboardButton(text="🧠 Features", callback_data="features")
        ],
        [
            InlineKeyboardButton(text="💳 Purchase", callback_data='purchase'),
            InlineKeyboardButton(text="⚙️ Commands", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="📣 Channel", url=get_groups()['main_channel_link']),
            InlineKeyboardButton(text="🛠 Support", url=get_admin()['link'])  
        ],
        [
            InlineKeyboardButton(text="✅ Vouches", url=get_groups()['vouches_LINK'])
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

def disactive_enter_message():
    return """🐉 <b>Dragon OTP Bot v2.0</b>
📡 <b>Status</b>: Fully Operational | ⏱️ <b>Uptime: 100%</b>

🚀 <b>Limited Access</b>: Only <u>few spots</u> remaining!

⚠️ <b>No Active Account Detected!</b>

🔐 To activate the bot, you must first <b>purchase subscription.</b>
💸 We recommend getting a <a href='https://t.me/chiroo4552'><b>SUBSCRIPTION BUNDLE</b></a> for <u>exclusive features</u> and the best <b>discounted price!</b>"""

def active_enter_message():
    return r"""👑 *Welcome In DRAGON OTP* — *Premium Access Activated* 🐉
    
🔥 You now have full access to the most advanced OTP spoofing system on the market

💼 Enjoy exclusive features
🚀 Ultra Fast Delivery
🧠 Custom Scripts & AI Voices
🎯 Highest Hit Rate in the Game
🎭 Spoofing Modes with Real\-Time Control
📂 Call Logs, Recording \& Dashboard Access

💎 You're not just a user\. You're part of the Dagon League
Let's dominate 💪"""

def sub_enter_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📜 Phonelist", callback_data="phonelist"),
            InlineKeyboardButton(text="🔥 Call Commands", callback_data="call_commands")
        ],
        [
            InlineKeyboardButton(text="🐉 Features", callback_data="features")
        ],
        [
            InlineKeyboardButton(text="💰 Purchase", callback_data='purchase'),
        ],
        [
            InlineKeyboardButton(text="🛠 Support", url=get_admin()['link'])  
        ],
        [
            InlineKeyboardButton(text="📣 Channel", url=get_groups()['main_channel_link']),
            InlineKeyboardButton(text="✅ Vouches", url=get_groups()['vouches_LINK'])
        ]
    ])

async def start_command(message: Message, bot:Bot):
    user_id = message.from_user.id
    name = message.from_user.first_name
    new,users_count = await is_new_user(user_id)
    if new:
        if message.from_user.username:
            username = "@"+message.from_user.username
        else:
            username = 'N/A'
        await bot.send_message(chat_id=get_admin()['id'],text=fr'''🆕 *New user*: {users_count}
*Username*\: {escape_markdown(username)}
*Name*\: `{escape_markdown(name)}`
*User ID*\: `{str(user_id)}`''',parse_mode='MarkdownV2')
    user_data = await get_user_cached(user_id)
    if not(user_data['banned']):
        if user_id == get_admin()['id']:
            await message.answer(admin_start_message(name), reply_markup=admin_start_keyboard(),parse_mode='MarkdownV2')
            return
        await message.answer_video(get_video(),caption=start_message(name), reply_markup=start_keyboard(),parse_mode='MarkdownV2')

async def start_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if not(user_data['banned']):
        name = callback.from_user.first_name
        if callback.data == 'back1':
            try:
                await callback.message.delete()
            except:
                pass
        else:
            try:
                for i in range(6):
                    await bot.delete_message(user_id,callback.message.message_id-i)
            except:
                pass
        await callback.message.answer_video(get_video(),caption=start_message(name), reply_markup=start_keyboard(),parse_mode='MarkdownV2')

async def enter_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:return
    member1 = await bot.get_chat_member(get_groups()['main_channel_ID'], user_id)
    member2 = await bot.get_chat_member(get_groups()['vouches_ID'], user_id)
    await callback.message.delete()
    if not (member1.status in ["member", "administrator", "creator"] and member2.status in ["member", "administrator", "creator"]):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📂 Add 'DRAGON 🐉' Folder" , url="https://t.me/addlist/WAoy34BFHyFlZTFk")
            ],
            [InlineKeyboardButton(text="✅ I've Subscribed", callback_data="subscribed")]
        ])
        await callback.message.answer(r'''⚠️ *You are not subscribed to our channels*

To use the bot, please subscribe to the required channels and group\.

👇 Click the button below to add them all in one folder and join easily:''',parse_mode='MarkdownV2',reply_markup=keyboard)
        return
    if check_subscription(user_data['expiry_date']) != True and user_id != get_admin()['id']:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 PURCHASE SUBSCRIPTION" , callback_data="purchase")
            ],
            [InlineKeyboardButton(text="🔙 Go Back ", callback_data="back1")]
        ])
        await callback.message.answer(disactive_enter_message(),reply_markup=keyboard,parse_mode='HTML',disable_web_page_preview=True)
        return
    
    await callback.message.answer_video(get_video(),caption=active_enter_message(),reply_markup=sub_enter_keyboard(), parse_mode='MarkdownV2')
    
async def subsribed_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:return
    member1 = await bot.get_chat_member(get_groups()['main_channel_ID'], user_id)
    member2 = await bot.get_chat_member(get_groups()['vouches_ID'], user_id)
    await callback.message.delete()
    if member1.status in ["member", "administrator", "creator"] and member2.status in ["member", "administrator", "creator"]:
        name = callback.from_user.first_name
        await callback.message.answer_video(get_video(),caption=start_message(name), reply_markup=start_keyboard(),parse_mode='MarkdownV2')
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Retry", callback_data="subscribed")],
        [InlineKeyboardButton(text="📂 Please Join to Channles" , url="https://t.me/addlist/WAoy34BFHyFlZTFk")]
            
        ])
    await callback.message.answer("""❌ You're still not subscribed!

Please join the required channels then click Retry.""",reply_markup=keyboard)

async def help_command(message: Message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])
    await message.answer("""DRAGON 𝙊𝙏𝙋 🐉 - 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 𝙃𝙚𝙡𝙥  𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 》 /redeem | 𝙍𝙚𝙙𝙚𝙚𝙢 𝙖 𝙠𝙚𝙮
🪙 》 /plan | 𝘾𝙝𝙚𝙘𝙠 𝙎𝙪𝙗𝙨𝙘𝙧𝙞𝙥𝙩𝙞𝙤𝙣 𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝙏𝙞𝙢𝙚
🪙 》 /phonelist | 𝘾𝙝𝙚𝙘𝙠 𝙇𝙞𝙨𝙩 𝙤𝙛 𝙇𝙖𝙩𝙚𝙨𝙩 𝙎𝙥𝙤𝙤𝙛 𝙉𝙪𝙢𝙗𝙚𝙧
🪙 》 /prices | 𝘾𝙝𝙚𝙘𝙠 𝙇𝙞𝙨𝙩 𝙤𝙛 𝙋𝙧𝙞𝙘𝙚𝙨
                                  
🪙 𝘾𝙖𝙡𝙡 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 》 /call | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘼𝙣𝙮 𝙘𝙤𝙙𝙚 
🪙 》 /citizens | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙞𝙩𝙞𝙯𝙚𝙣𝙨 𝙊𝙏𝙋 𝙘𝙤𝙙𝙚
🪙 》 /creditcard | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙧𝙚𝙙𝙞𝙩 𝘾𝙖𝙧𝙙 ( 𝘾𝘾 ) 𝙊𝙏𝙋 𝙘𝙤𝙙𝙚                                                                                                                                                               
🪙 》 /applepay | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙊𝙏𝙋 𝘾𝙧𝙚𝙙𝙞𝙩 𝘾𝙖𝙧𝙙
🪙 》 /coinbase | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 2𝙁𝘼 𝘾𝙤𝙙𝙚
🪙 》 /amazon | 𝘼𝙥𝙥𝙧𝙤𝙫𝙖𝙡 𝘼𝙪𝙩𝙝𝙚𝙣𝙩𝙞𝙘𝙖𝙩𝙞𝙤𝙣
🪙 》 /microsoft | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙈𝙞𝙘𝙧𝙤𝙨𝙤𝙛𝙩 𝘾𝙤𝙙𝙚
🪙 》 /paypal | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙋𝙖𝙮𝙥𝙖𝙡 𝘾𝙤𝙙𝙚
🪙 》 /venmo | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙑𝙚𝙣𝙢𝙤 𝘾𝙤𝙙𝙚
🪙 》 /ssn | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙎𝙎𝙉 𝙛𝙧𝙤𝙢 𝙫𝙞𝙘𝙩𝙞𝙢                                    
🪙 》 /cashapp | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙖𝙨𝙝𝙖𝙥𝙥 𝘾𝙤𝙙𝙚
🪙 》 /quadpay | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙦𝙪𝙖𝙙𝙥𝙖𝙮 𝘾𝙤𝙙𝙚
🪙 》 /carrier | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙘𝙖𝙧𝙧𝙞𝙚𝙧 𝘾𝙤𝙙𝙚

                                      
🪙  𝘾𝙪𝙨𝙩𝙤𝙢 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨
                                      
🪙 》 /createscript | 𝘾𝙧𝙚𝙖𝙩𝙚 𝙔𝙤𝙪𝙧 𝘾𝙪𝙨𝙩𝙤𝙢 𝙎𝙘𝙧𝙞𝙥𝙩
🪙 》 /script | 𝙑𝙞𝙚𝙬 𝙨𝙘𝙧𝙞𝙥𝙩                                 
🪙 》 /customcall | 𝘾𝙖𝙡𝙡 𝙬𝙞𝙩𝙝 𝙔𝙤𝙪𝙧 𝙨𝙘𝙧𝙞𝙥𝙩                                  
🪙 》 /customvoice | 𝘾𝙖𝙡𝙡 𝙬𝙞𝙩𝙝 𝙔𝙤𝙪𝙧 𝙨𝙘𝙧𝙞𝙥𝙩 𝙖𝙣𝙙 𝙈𝙤𝙙𝙞𝙛𝙮 𝙇𝙖𝙣𝙜𝙪𝙖𝙜𝙚 𝘼𝙣𝙙 𝙑𝙤𝙞𝙘𝙚
🪙 》 /voicelist | 𝘾𝙝𝙚𝙘𝙠 𝙡𝙖𝙣𝙜𝙪𝙖𝙜𝙚 𝙖𝙣𝙙 𝙑𝙤𝙞𝙘𝙚𝙨 𝙇𝙞𝙨𝙩 
🪙 𝙀𝙭𝙩𝙧𝙖𝙨
🪙  》/recall | 𝙛𝙤𝙧 𝙧𝙚 𝙘𝙖𝙡𝙡𝙞𝙣𝙜  

🪙 𝙎𝙚𝙘𝙪𝙧𝙚 𝙔𝙤𝙪𝙧 𝙆𝙚𝙮 
     
🪙/purchase | 𝙏𝙤 𝘽𝙪𝙮 𝙆𝙚𝙮""", reply_markup=keyboard)

async def help_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("""DRAGON 𝙊𝙏𝙋 🐉 - 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 𝙃𝙚𝙡𝙥  𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 》 /redeem | 𝙍𝙚𝙙𝙚𝙚𝙢 𝙖 𝙠𝙚𝙮
🪙 》 /plan | 𝘾𝙝𝙚𝙘𝙠 𝙎𝙪𝙗𝙨𝙘𝙧𝙞𝙥𝙩𝙞𝙤𝙣 𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝙏𝙞𝙢𝙚
🪙 》 /phonelist | 𝘾𝙝𝙚𝙘𝙠 𝙇𝙞𝙨𝙩 𝙤𝙛 𝙇𝙖𝙩𝙚𝙨𝙩 𝙎𝙥𝙤𝙤𝙛 𝙉𝙪𝙢𝙗𝙚𝙧
🪙 》 /prices | 𝘾𝙝𝙚𝙘𝙠 𝙇𝙞𝙨𝙩 𝙤𝙛 𝙋𝙧𝙞𝙘𝙚𝙨
                                  
🪙 𝘾𝙖𝙡𝙡 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 》 /call | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘼𝙣𝙮 𝙘𝙤𝙙𝙚 
🪙 》 /citizens | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙞𝙩𝙞𝙯𝙚𝙣𝙨 𝙊𝙏𝙋 𝙘𝙤𝙙𝙚
🪙 》 /creditcard | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙧𝙚𝙙𝙞𝙩 𝘾𝙖𝙧𝙙 ( 𝘾𝘾 ) 𝙊𝙏𝙋 𝙘𝙤𝙙𝙚                                                                                                                                                               
🪙 》 /applepay | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙊𝙏𝙋 𝘾𝙧𝙚𝙙𝙞𝙩 𝘾𝙖𝙧𝙙
🪙 》 /coinbase | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 2𝙁𝘼 𝘾𝙤𝙙𝙚
🪙 》 /amazon | 𝘼𝙥𝙥𝙧𝙤𝙫𝙖𝙡 𝘼𝙪𝙩𝙝𝙚𝙣𝙩𝙞𝙘𝙖𝙩𝙞𝙤𝙣
🪙 》 /microsoft | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙈𝙞𝙘𝙧𝙤𝙨𝙤𝙛𝙩 𝘾𝙤𝙙𝙚
🪙 》 /paypal | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙋𝙖𝙮𝙥𝙖𝙡 𝘾𝙤𝙙𝙚
🪙 》 /venmo | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙑𝙚𝙣𝙢𝙤 𝘾𝙤𝙙𝙚
🪙 》 /ssn | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙎𝙎𝙉 𝙛𝙧𝙤𝙢 𝙫𝙞𝙘𝙩𝙞𝙢                                    
🪙 》 /cashapp | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙖𝙨𝙝𝙖𝙥𝙥 𝘾𝙤𝙙𝙚
🪙 》 /quadpay | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙦𝙪𝙖𝙙𝙥𝙖𝙮 𝘾𝙤𝙙𝙚
🪙 》 /carrier | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙘𝙖𝙧𝙧𝙞𝙚𝙧 𝘾𝙤𝙙𝙚

                                      
🪙  𝘾𝙪𝙨𝙩𝙤𝙢 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨
                                      
🪙 》 /createscript | 𝘾𝙧𝙚𝙖𝙩𝙚 𝙔𝙤𝙪𝙧 𝘾𝙪𝙨𝙩𝙤𝙢 𝙎𝙘𝙧𝙞𝙥𝙩
🪙 》 /script | 𝙑𝙞𝙚𝙬 𝙨𝙘𝙧𝙞𝙥𝙩                                 
🪙 》 /customcall | 𝘾𝙖𝙡𝙡 𝙬𝙞𝙩𝙝 𝙔𝙤𝙪𝙧 𝙨𝙘𝙧𝙞𝙥𝙩                                  
🪙 》 /customvoice | 𝘾𝙖𝙡𝙡 𝙬𝙞𝙩𝙝 𝙔𝙤𝙪𝙧 𝙨𝙘𝙧𝙞𝙥𝙩 𝙖𝙣𝙙 𝙈𝙤𝙙𝙞𝙛𝙮 𝙇𝙖𝙣𝙜𝙪𝙖𝙜𝙚 𝘼𝙣𝙙 𝙑𝙤𝙞𝙘𝙚
🪙 》 /voicelist | 𝘾𝙝𝙚𝙘𝙠 𝙡𝙖𝙣𝙜𝙪𝙖𝙜𝙚 𝙖𝙣𝙙 𝙑𝙤𝙞𝙘𝙚𝙨 𝙇𝙞𝙨𝙩 
🪙 𝙀𝙭𝙩𝙧𝙖𝙨
🪙  》/recall | 𝙛𝙤𝙧 𝙧𝙚 𝙘𝙖𝙡𝙡𝙞𝙣𝙜  

🪙 𝙎𝙚𝙘𝙪𝙧𝙚 𝙔𝙤𝙪𝙧 𝙆𝙚𝙮 
     
🪙/purchase | 𝙏𝙤 𝘽𝙪𝙮 𝙆𝙚𝙮""", reply_markup=keyboard)

async def features_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 GO BACK", callback_data="back1")]
    ])
    await callback.message.delete()
    await callback.message.answer_video(get_video(),caption=r"""🐉 *UNIQUE FEATURES*

🚀 Lightning Fast OTP Delivery  
🎭 Custom Caller ID \(Spoofing Mode\)  
🔊 AI Voice Calls with Human Detection  
📞 Call Any Number Worldwide  
📦 Multiple OTP Services Supported  
📁 Live Call Recording & Logs  
📊 Real\-Time Dashboard & Analytics  
🔐 Encrypted Access & Security  
📲 Use Anywhere Anytime""",reply_markup=keyboard,parse_mode='MarkdownV2')

async def call_commands_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 GO BACK", callback_data="back1")]
    ])
    await callback.message.delete()
    await callback.message.answer(r"""🪙 𝘾𝙖𝙡𝙡 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

🪙 》 /call | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘼𝙣𝙮 𝙘𝙤𝙙𝙚 
🪙 》 /citizens | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙞𝙩𝙞𝙯𝙚𝙣𝙨 𝙊𝙏𝙋 𝙘𝙤𝙙𝙚
🪙 》 /creditcard | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙧𝙚𝙙𝙞𝙩 𝘾𝙖𝙧𝙙 ( 𝘾𝘾 ) 𝙊𝙏𝙋 𝙘𝙤𝙙𝙚                                                                                                                                                               
🪙 》 /applepay | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙊𝙏𝙋 𝘾𝙧𝙚𝙙𝙞𝙩 𝘾𝙖𝙧𝙙
🪙 》 /coinbase | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 2𝙁𝘼 𝘾𝙤𝙙𝙚
🪙 》 /amazon | 𝘼𝙥𝙥𝙧𝙤𝙫𝙖𝙡 𝘼𝙪𝙩𝙝𝙚𝙣𝙩𝙞𝙘𝙖𝙩𝙞𝙤𝙣
🪙 》 /microsoft | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙈𝙞𝙘𝙧𝙤𝙨𝙤𝙛𝙩 𝘾𝙤𝙙𝙚
🪙 》 /paypal | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙋𝙖𝙮𝙥𝙖𝙡 𝘾𝙤𝙙𝙚
🪙 》 /venmo | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙑𝙚𝙣𝙢𝙤 𝘾𝙤𝙙𝙚
🪙 》 /ssn | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙎𝙎𝙉 𝙛𝙧𝙤𝙢 𝙫𝙞𝙘𝙩𝙞𝙢                                    
🪙 》 /cashapp | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝘾𝙖𝙨𝙝𝙖𝙥𝙥 𝘾𝙤𝙙𝙚
🪙 》 /quadpay | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙦𝙪𝙖𝙙𝙥𝙖𝙮 𝘾𝙤𝙙𝙚
🪙 》 /carrier | 𝘾𝙖𝙥𝙩𝙪𝙧𝙚 𝙘𝙖𝙧𝙧𝙞𝙚𝙧 𝘾𝙤𝙙𝙚                               
🪙 》 /customcall | 𝘾𝙖𝙡𝙡 𝙬𝙞𝙩𝙝 𝙔𝙤𝙪𝙧 𝙨𝙘𝙧𝙞𝙥𝙩                                  
🪙 》 /customvoice | 𝘾𝙖𝙡𝙡 𝙬𝙞𝙩𝙝 𝙔𝙤𝙪𝙧 𝙨𝙘𝙧𝙞𝙥𝙩 𝙖𝙣𝙙 𝙈𝙤𝙙𝙞𝙛𝙮 𝙇𝙖𝙣𝙜𝙪𝙖𝙜𝙚 """,reply_markup=keyboard)
    
async def phonelist_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 GO BACK", callback_data="back1")]
    ])
    await callback.message.delete()
    await callback.message.answer(spoof_message(),reply_markup=keyboard)
