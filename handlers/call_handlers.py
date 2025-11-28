import random
from random import randint
import ast
import asyncio
from aiogram.types import Message, CallbackQuery
from utils import get_user_cached, update_user_cache,db, get_spoofer_number, check_subscription, is_valid_phone_number, is_name_valid, check_spoof, escape_markdown, get_region_language, get_service_name
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import get_spoofing, spoof_message, get_admin, get_error, get_spoofing_services

def ringing_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Accept ✅", callback_data='acp'),
            InlineKeyboardButton(text="Deny ❌", callback_data="den"),
        ],
        [
            InlineKeyboardButton(text="💵 SNN", callback_data='acp'),
            InlineKeyboardButton(text="✉ EMAIL", callback_data='acp')
        ],
        [
            InlineKeyboardButton(text="📱 WhatsApp", callback_data="acp"),
            InlineKeyboardButton(text="📌 Pin", callback_data="acp")
        ],
        [
            InlineKeyboardButton(text="📲 Auth App", callback_data='acp'),
            InlineKeyboardButton(text="🏦 Account No.", callback_data='acp')
        ],
        [
            InlineKeyboardButton(text="🔁 Routing No.", callback_data='rout'),
            InlineKeyboardButton(text="💳 Card Number", callback_data="card")]
        ,
        [
            InlineKeyboardButton(text="📩 WhatsApp Code", callback_data='acp'),
            InlineKeyboardButton(text="🔒 CVV", callback_data="cvv")]
            ,
        [
            InlineKeyboardButton(text="📅 Expiry Date", callback_data='acp'),
            InlineKeyboardButton(text="📨 Push Notification", callback_data="acp")]
    ])

def unsubscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Purchase", callback_data="purchase")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])

async def call_proccess(message, parts, user_id):
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    if check_subscription(user_data['expiry_date']) != True and user_id != get_admin()['id']:
        await message.answer('No Subscriptions Found ❌', reply_markup=unsubscriber_keyboard())
        return
    if len(parts) < 6:
        await message.answer(fr"""❌ Invalid command format\.
`{parts[0]} 15087144578 18888888888 Paypal John 6`""",
                             parse_mode="MarkdownV2")
        return
    victim_number, spoof_number, service_name, victim_name, otp_digit = (
        parts[1], parts[2], parts[3], parts[4], parts[5])
    if (is_valid_phone_number(victim_number)
            and victim_number not in get_spoofing()
            and is_valid_phone_number(spoof_number)
            and check_spoof(spoof_number, service_name, victim_name) == True
            and is_name_valid(victim_name) and 4 <= int(otp_digit) <= 12):
        await update_user_cache(user_id, 'last_call',str(parts))
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="End Call", callback_data="end_call")
            ]])
        if parts[0] == '/call':
            await message.answer(fr"""╔═══ 📞 *CALL INITIATED* ═══╗
🔰  *New spoofed call started*
╚════════════════╝

👤 *Target Name*: {victim_name}
📲 *Target Number*: \{victim_number}
🌎 *Location*: {escape_markdown(get_region_language(victim_number))}
🎭 *From*: \{spoof_number}
🎟 *Service*: {service_name}
🔢 *OTP Digits Expected*: {otp_digit}

━━━━━━━━━━━━━━━
📡 *Status*: 🟢 *Active*""",reply_markup=keyboard,parse_mode='MarkdownV2')
        if parts[0] == '/customcall':
            await message.answer(fr"""╔═══ 📞 *CALL INITIATED* ═══╗
🔰  *New spoofed call started*
╚════════════════╝

👤 *Target Name*: {victim_name}
📲 *Target Number*: \{victim_number}
🌎 *Location*: {escape_markdown(get_region_language(victim_number))}
🎭 *From*: \{spoof_number}
🎟 *Service*: {service_name}
📜 *Custom Script*: On 
🔢 *OTP Digits Expected*: {otp_digit}

━━━━━━━━━━━━━━━
📡 *Status*: 🟢 *Active*""",reply_markup=keyboard,parse_mode='MarkdownV2')
        if parts[0] == '/customvoice':
            await message.answer(fr"""╔═══ 📞 *CALL INITIATED* ═══╗
🔰  *New spoofed call started*
╚════════════════╝

👤 *Target Name*: {victim_name}
📲 *Target Number*: \{victim_number}
🌎 *Location*: {escape_markdown(get_region_language(victim_number))}
🎭 *From*: \{spoof_number}
🎟 *Service*: {service_name}
📜 *Custom Script*: On 
🗣 *Voice*: {user_data['voice']}
🔢 *OTP Digits Expected*: {otp_digit}

━━━━━━━━━━━━━━━
📡 *Status*: 🟢 *Active*""",reply_markup=keyboard,parse_mode='MarkdownV2')
        if user_id == get_admin()['id']:
            await asyncio.sleep(randint(11, 19))
            await message.answer(fr"🌐 Call Answered")
            await asyncio.sleep(randint(3, 5))
            await message.answer("👤 Human detected")
            await asyncio.sleep(randint(3, 5))
            await message.answer(f"📲 {escape_markdown(victim_name)} pressed 1, Send OTP...")
            await asyncio.sleep(randint(8, 20))
            chars = '0123456789'
            code = ''.join(random.choices(chars, k=int(otp_digit)))
            for i in range(int(otp_digit)):
                await message.answer(f"{victim_name} Pressed 📲 : {code[i]}")
                await asyncio.sleep(randint(1, 2))
            await message.answer(f"✅ CODE: {code}",
                                 reply_markup=ringing_keyboard())
            return
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])
        ]])
        await asyncio.sleep(randint(0, 2))
        await message.answer('❌ *Unable to start the call*',
                             parse_mode="MarkdownV2")
        await message.answer(get_error(),
                             reply_markup=keyboard,
                             parse_mode="MarkdownV2")
        return
    await message.answer(fr"""❌ Oops... Something went wrong!""")

async def call_command(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if parts[0] in ['/call','/customcall','/customvoice']:
        await call_proccess(message, parts, user_id)
        return
    if parts[0] == '/recall':
        user_data = await get_user_cached(user_id)
        
        if user_data['last_call'] == 'N/A':
            await message.answer(
                "⚠️ No saved call found. Please use /call first.")
            return
        args = ast.literal_eval(user_data['last_call'])
        if args[0] == '/call':
            await call_proccess(message, args, user_id)
            return
        if args[0] == '/repportcall':
            await repcall_proccess(message, args, user_id)
            return
        await precall_proccess(message, args, user_id)
        return
    if parts[0] == '/repportcall':
        await repcall_proccess(message, parts, user_id)
        return
    await precall_proccess(message, parts, user_id)

async def precall_proccess(message, parts, user_id):
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    if check_subscription(user_data['expiry_date']) != True and user_id != get_admin()['id']:
        await message.answer('No Subscriptions Found ❌', reply_markup=unsubscriber_keyboard())
        return
    if len(parts) < 4:
        await message.answer(fr"""❌ Invalid command format\.
`{parts[0]} 15087144578 John 6`""",
                             parse_mode="MarkdownV2")
        return
    victim_number, victim_name, otp_digit = (parts[1], parts[2], parts[3])
    if (is_valid_phone_number(victim_number)
            and victim_number not in get_spoofing()
            and is_name_valid(victim_name) and 4 <= int(otp_digit) <= 12):
        await update_user_cache(user_id, 'last_call',str(parts))
        spoof_number = get_spoofer_number(parts[0][1:])

        await message.answer(fr"""╔═══ 📞 *CALL INITIATED* ═══╗
🔰  *New spoofed call started*
╚════════════════╝

👤 *Target Name*: {victim_name}
📲 *Target Number*: \{victim_number}
🌎 *Location*: {escape_markdown(get_region_language(victim_number))}
🎭 *From*: \{spoof_number}
🎟 *Service*: {parts[0][1:]}
🔢 *OTP Digits Expected*: {otp_digit}

━━━━━━━━━━━━━━━
📡 *Status*: 🟢 *Active*""",
                             parse_mode='MarkdownV2')
        if user_id == get_admin()['id']:
            await asyncio.sleep(randint(11, 19))
            await message.answer(fr"🌐 Call Answered")
            await asyncio.sleep(randint(3, 5))
            await message.answer("👤 Human detected")
            await asyncio.sleep(randint(3, 5))
            await message.answer(f"📲 {escape_markdown(victim_name)} pressed 1, Send OTP...")
            await asyncio.sleep(randint(8, 20))
            chars = '0123456789'
            code = ''.join(random.choices(chars, k=int(otp_digit)))
            for i in range(int(otp_digit)):
                await message.answer(f"{victim_name} Pressed 📲 : {code[i]}")
                await asyncio.sleep(randint(0, 1))
            await message.answer(f"✅ *CODE*: `{code}`",
                                 reply_markup=ringing_keyboard(),
                                 parse_mode='MarkdownV2')
            return
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])
        ]])
        await asyncio.sleep(randint(0, 2))
        await message.answer('❌ *Unable to start the call*',
                             parse_mode="MarkdownV2")
        await message.answer(get_error(),
                             reply_markup=keyboard,
                             parse_mode="MarkdownV2")
        return
    await message.answer(fr"""❌ Oops... Something went wrong!""")

async def otp_accept_callback(callback: CallbackQuery):
    msg = callback.message.text
    msg = f'✅ CODE: {msg[8:]}'
    user_data = await get_user_cached(callback.from_user.id)
    if callback.data == 'acp':
        await callback.message.edit_text(fr'''{msg}
🔑 Code has Been accepted''')
        await asyncio.sleep(1, 2)
        await callback.message.answer('☎ Call has ended.\nPress /recall To Recall.')
    if callback.data == 'den':
        await callback.message.edit_text(fr'''{msg}
❌ Code has been rejected''')
        await callback.message.answer('🛰 Placin victim back to IVR')
        await asyncio.sleep(randint(8, 20))
        chars = '0123456789'
        parts =ast.literal_eval(user_data['last_call'])
        code = ''.join(random.choices(chars, k=int(parts[-1])))
        for i in range(int(parts[-1])):
            await callback.message.answer(f"{parts[-2]} Pressed 📲 : {code[i]}")
            await asyncio.sleep(randint(1, 2))
        await callback.message.answer(f"✅ CODE: {code}",
                                reply_markup=ringing_keyboard())
    if callback.data == 'card':
        await callback.message.edit_text(fr'''{msg}
💳 Card number has been required''')
        await callback.message.answer('🛰 Placin victim back to IVR')
        await asyncio.sleep(randint(8, 20))
        chars = '0123456789'
        parts =ast.literal_eval(user_data['last_call'])
        code = ''.join(random.choices(chars, k=16))
        for i in range(16):
            await callback.message.answer(f"{parts[-2]} Pressed 📲 : {code[i]}")
            await asyncio.sleep(randint(1, 2))
        await callback.message.answer(f"✅ CODE: {code}",
                                reply_markup=ringing_keyboard())
    if callback.data == 'cvv':
        await callback.message.edit_text(fr'''{msg}
🔒 Cvv security code has been required''')
        await callback.message.answer('🛰 Placin victim back to IVR')
        await asyncio.sleep(randint(8, 20))
        chars = '0123456789'
        parts =ast.literal_eval(user_data['last_call'])
        code = ''.join(random.choices(chars, k=3))
        for i in range(3):
            await callback.message.answer(f"{parts[-2]} Pressed 📲 : {code[i]}")
            await asyncio.sleep(randint(1, 2))
        await callback.message.answer(f"✅ CODE: {code}",
                                reply_markup=ringing_keyboard())
    if callback.data == 'rout':
        await callback.message.edit_text(fr'''{msg}
🔁 Routing number has been required''')
        await callback.message.answer('🛰 Placin victim back to IVR')
        await asyncio.sleep(randint(8, 20))
        chars = '0123456789'
        parts =ast.literal_eval(user_data['last_call'])
        code = ''.join(random.choices(chars, k=9))
        for i in range(9):
            await callback.message.answer(f"{parts[-2]} Pressed 📲 : {code[i]}")
            await asyncio.sleep(randint(1, 2))
        await callback.message.answer(f"✅ CODE: {code}",
                                reply_markup=ringing_keyboard())

async def Phonelist_commands(message: Message):
    user_id = message.from_user.id
    if await db.get_user_info(user_id, 'banned'): return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")
    ]])
    await message.answer(spoof_message(),
                         reply_markup=keyboard)

async def repcall_proccess(message, parts, user_id):
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    if check_subscription(user_data['expiry_date']) != True and user_id != get_admin()['id']:
        await message.answer('No Subscriptions Found ❌', reply_markup=unsubscriber_keyboard())
        return
    if user_data['rep'] != True:
        await message.answer(
            r"""⚠️ *Access Restricted* — You have an active subscription, but this command requires an *additional option* that is not included in your plan\.  
Please upgrade or purchase the required option to continue\.""",
            parse_mode='MarkdownV2')
        return
    if len(parts) < 7:
        await message.answer(fr"""❌ Invalid command format\.
`{parts[0]} 15087144578 18888888888 Paypal John M Y`""",
                             parse_mode="MarkdownV2")
        return
    company_number, user_number, service_name, user_name, user_sex, methode = (
        parts[1], parts[2], parts[3], parts[4], parts[5], parts[6])
    if (company_number not in get_spoofing()
            and user_number not in get_spoofing()
            and company_number != user_number
            and is_name_valid(user_name)
            and user_name.upper() not in get_spoofing_services()
            and user_sex.upper() in ['F', 'M']
            and methode.upper() in ['Y', 'N']):
        await update_user_cache(user_id, 'last_call',str(parts))
        await message.answer(fr"📴 Configure the number `{user_number}`",
                             parse_mode='MarkdownV2')
        await asyncio.sleep(randint(10, 20))
        await message.answer(fr"📞 Phone number configurated Successfully!")
        await asyncio.sleep(randint(0, 5))
        if user_sex.upper() == 'M':
            voice = 'Michael'
        else:
            voice = 'Mia'
        await message.answer(fr"""╔═══ 📞 *CALL INITIATED* ═══╗
🔰  *New spoofed call started*
╚════════════════╝

👤 *Target Name*: {service_name}
📲 *Target Number*: \{user_number}
🌎 *Location*: {escape_markdown(get_region_language(user_number))}
🎭 *From*: \{user_number}
🎟 *Service*: {parts[0][1:]}
🗣 *Voice* : {voice}

━━━━━━━━━━━━━━━
📡 *Status*: 🟢 *Active*""",
                             parse_mode='MarkdownV2')
        if user_id == get_admin()['id']:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="End Call", callback_data="end_call")
            ]])
            await asyncio.sleep(randint(0, 2))
            await message.answer("📞 *CALL RINGING*",
                                 reply_markup=keyboard,
                                 parse_mode='MarkdownV2')
            await asyncio.sleep(randint(3, 6))
            await message.answer(
                fr"🤳 *{escape_markdown(service_name)} Agent* Answered The Call\.",
                parse_mode='MarkdownV2')
            await asyncio.sleep(randint(3, 5))
            await message.answer("🔇 Silent *Human* detection",
                                 parse_mode='MarkdownV2')
            await asyncio.sleep(randint(3, 5))
            await message.answer(fr"🤖 *Bot* runs the script\.\.\.",
                                 parse_mode='MarkdownV2')
            await asyncio.sleep(randint(8, 20))
            await message.answer(fr"🗣 Talikng About it\.\.\.",
                                 parse_mode='MarkdownV2')
            await asyncio.sleep(randint(8, 20))
            if methode.upper() == 'N':
                await message.answer(fr"✅ *Everything* is Done\!",
                                     parse_mode='MarkdownV2')
                await asyncio.sleep(1, 2)
                file_id = 'CQACAgQAAxkDAAIliGkGRF_mGswlQ3rQHKZ2yrdElXzuAALnHgACpOoxUO_yqMXmyY-xNgQ'
                await message.answer(
                    '☎ Call has ended.\nPress /recall To Recall.')
                await asyncio.sleep(2, 5)
                await message.answer_audio(file_id)
            else:
                chars = '0123456789'
                code = ''.join(random.choices(chars, k=int(6)))
                await message.answer(f"✅ *CODE*: `{code}`",
                                     reply_markup=ringing_keyboard(),
                                     parse_mode='MarkdownV2')
            return
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])
        ]])
        await asyncio.sleep(randint(0, 2))
        await message.answer('❌ *Unable to start the call*',
                             parse_mode="MarkdownV2")
        await message.answer(get_error(),
                             reply_markup=keyboard,
                             parse_mode="MarkdownV2")
        return
    await message.answer(fr"❌ Oops... Something went wrong!")

