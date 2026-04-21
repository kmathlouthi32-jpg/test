import random
from random import randint
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram.types import Message, CallbackQuery
from utils import update_user_cache, remove_backslashes, mask_phone_number, get_random_caller, get_user_cached, check_subscription, is_valid_phone_number, is_name_valid, escape_markdown_user
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import get_spoofing, get_admin
import ast
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

def build_script_keyboard(options, custom_scripts):
    rows = []
    for i in range(0, len(options), 2):
        pair = options[i:i+2]   # slice never raises, gives 1 or 2 items
        row = [{"text": opt, "callback_data": "call_script_" + opt} for opt in pair]
        rows.append(row)

    custom_scripts = custom_scripts[:5]
    if custom_scripts:
        rows.append([{"text": "—— Custom Script ——", "callback_data": "empty"}])
        for i in range(0, len(custom_scripts), 2):
            pair = custom_scripts[i:i+2]
            row = []
            for s in pair:
                first_line = s.splitlines()[0]
                row.append({"text": first_line, "callback_data": "call_script_" + first_line})
            rows.append(row)

    rows.append([{"text": "⬅ Back", "callback_data": "start_back"}])

    return {"inline_keyboard": rows}

async def call_proccess(message, parts, user_id, script=None):
    user_data = get_user_cached(user_id)
    if check_subscription(user_data['expiry_date']) != True and user_id != get_admin()['id']:
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "📦 Buy a Subscription",
            "callback_data": "spoof_packages"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "start_back"
        }
        ]
    ]
    }
        await message.answer('''❌ You need a subscription to make calls.

use 📦 Buy a Subscription bellow.''', reply_markup=keyboard)
        return
    if len(parts) != 6 and len(parts) != 5:
        await message.answer('❌ Invalid command format.')
        return
    if len(parts) == 5:
        victim_number, service_name, victim_name, otp_digit = (
        parts[1], parts[2], parts[3], parts[4])
        if user_data['caller_id'] != 'Fixed':
            caller_id = get_random_caller()
        else:
            if (check_subscription(user_data['spoof'])==True) or user_id == get_admin()['id']:
                if user_data['my_number'] != 'Not set':
                    caller_id = user_data['my_number']
                else:
                    caller_id = get_random_caller()
            else:
                keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🎭 Buy a Spoofing package",
            "callback_data": "subscriptions"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "start_back"
        }
        ]
    ]
    }
                await message.answer('''❌ You need a spoofing package to make calls with fixed caller id.

use 🎭 Buy a Spoofing package bellow.''', reply_markup=keyboard)
                return
    else:
        victim_number,entred_number, service_name, victim_name, otp_digit = (
        parts[1], parts[2], parts[3], parts[4], parts[5])
        if entred_number[0] != '+':
            entred_number = '+'+entred_number
        if user_data['caller_id'] != 'Fixed':
            if (check_subscription(user_data['spoof'])==True) or user_id == get_admin()['id']:
                if is_valid_phone_number(entred_number):
                    caller_id = entred_number
                else:
                    caller_id = get_random_caller()
            else:
                caller_id = get_random_caller()
        else:
            if (check_subscription(user_data['spoof'])==True) or user_id == get_admin()['id']:
                if user_data['my_number'] != 'Not set':
                    caller_id = user_data['my_number']
                else:
                    if is_valid_phone_number(entred_number):
                        caller_id = entred_number
                    else:
                        caller_id = get_random_caller()
            else:
                keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🎭 Buy a Spoofing package",
            "callback_data": "subscriptions"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "start_back"
        }
        ]
    ]
    }
                await message.answer('''❌ You need a spoofing package to make calls with fixed caller id.

use 🎭 Buy a Spoofing package bellow.''', reply_markup=keyboard)
                return

    if victim_number[0] != '+':
        victim_number = "+"+victim_number
    if caller_id[0] != '+':
        caller_id = "+"+caller_id

    if (is_valid_phone_number(victim_number) and victim_number not in get_spoofing() and is_name_valid(victim_name) and 4 <= int(otp_digit) <= 12):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="❌ End Call", callback_data="end_call")
            ]])
        if script == None:
            script_to_use = user_data['script']
        else:
            script_to_use = script
        await update_user_cache(user_id, 'in_call', True)
        await update_user_cache(user_id, 'last_call', str(parts))
        

        text = fr"""📞 *Calling\.\.\.*
            
📱 *Target*: {escape_markdown_user(mask_phone_number(victim_number))}
📞 *From*: {escape_markdown_user(caller_id)}
🏢 *Service*: {escape_markdown_user(service_name)}
📜 *Script*: {escape_markdown_user(script_to_use)}
👤 *Contact*: {escape_markdown_user(victim_name)}
🔢 *OTP Digits*: {otp_digit}"""
        if script == None:
            await message.answer(text,reply_markup=keyboard,parse_mode='MarkdownV2')
        else:
            await message.edit_text(text,reply_markup=keyboard,parse_mode='MarkdownV2')
        await asyncio.sleep(randint(5, 10))
        
        if user_id == get_admin()['id']:
            await asyncio.sleep(randint(11, 19))
            await message.answer(fr"📞 Calling {victim_number[1:]}")
            await message.answer(fr"🔔 Ringing...")
            await asyncio.sleep(randint(3, 5))
            await message.answer("🧑 Human detected - starting script...")
            await asyncio.sleep(randint(10, 15))
            await message.answer(f"✅ Confirm, {victim_name} pressed 1, Send OTP...")
            await message.answer(f"⏳ Waiting for code...")
            await asyncio.sleep(randint(8, 20))
            chars = '0123456789'
            code = ''.join(random.choices(chars, k=int(otp_digit)))
            for i in range(int(otp_digit)):
                await message.answer(f"{victim_name} Pressed 📲 : {code[i]}")
                await asyncio.sleep(randint(1, 3))
            await message.answer(f"""🔑 Code received: {code}

Accept or Deny?""", reply_markup=ringing_keyboard())
            await update_user_cache(user_id, 'in_call', False)
            return
        
        await message.answer('🔴 Call ended.')
        await asyncio.sleep(1)
        await message.answer('🔴 Call failed: Call rejected by telegram API.')
        await message.answer('🔴 Call ended (0s)')
        await asyncio.sleep(1)
        text = fr"""📞 *Call Ended*
            
🏢 *Service*: {escape_markdown_user(service_name)}
👤 *Contact*: {escape_markdown_user(victim_name)}
⏳ *Duration*: 0s
🔢 *Code\(s\)*: `None`"""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🔄 Recall",
            "callback_data": "recall"
        }
        ],
        [
        {
            "text": "⬅ Main Menu",
            "callback_data": "start_back"
        }
        ]
    ]
    }
        await message.answer(text,reply_markup=keyboard,parse_mode='MarkdownV2')
        await update_user_cache(user_id, 'in_call', False)
        return

    await message.answer('‼️ Please check your command and try again.')


# --- STATE DEFINITION ---
class callForm(StatesGroup):
    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_service = State()
    waiting_for_confirmation = State()



async def recall_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    data = user_data['last_call']
    parts = ast.literal_eval(data)
    await call_proccess(callback.message, parts, user_id)

async def call_command(message: Message):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] or user_data['in_call']:return
    parts = message.text.split()
    await call_proccess(message, parts, user_id)
    

async def call_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    options = [
    "Default",
    "Bank Security",
    "Delivery",
    "Amazon",
    "PayPal",
    "Crypto Exchange",
    "Insurance",
    "Telecom",
    "Email Security",
    "Tax Authority",
    "Marcus - Unauthorized Transfer",
    "Marcus - Login Alert",
    "Marcus - CD Withdrawal",
    "Marcus - Personal Loan",
    "Barclays - Fraud Alert",
    "Barclays - Login Alert",
    "Barclays - Wire Transfer",
    "Truist - Fraud Alert",
    "Truist - Account Access",
    "Truist - Zelle Transfer",
    "ID.me - Identity Verification",
    "ID.me - Suspicious Login",
    "ID.me - Benefits Verification",
    "Apple",
    "Google",
    "Microsoft",
    "Chase Bank",
    "Wells Fargo",
    "Bank of America",
    "Venmo",
    "Cash App",
    "Zelle",
    'ID.ME - Login Alert'
]
    scripts = []
    user_data = get_user_cached(user_id)
    for i in range(1,6):
        if user_data['cus_script'+str(i)] != 'N/A':
            clean_script = user_data['cus_script'+str(i)].splitlines()[0]
            clean_script = clean_script[3:len(clean_script)-1]
            scripts.append(remove_backslashes(clean_script))
    keyboard = build_script_keyboard(options, scripts)
    await callback.message.edit_text('📜 Select the script.', reply_markup=keyboard)

async def waiting_for_script_state(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    script = callback.data[12:]
    await state.update_data(script=script)
    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel call", "callback_data": "start_back"}]
        ]
    }
    await callback.message.edit_text('📱 Send victim number.', reply_markup=keyboard)

    await state.set_state(callForm.waiting_for_number)

async def waiting_for_number_state(message:Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel call", "callback_data": "start_back"}]
        ]
    }
    number = message.text
    if number[0] != '+':
        number = '+'+number
    if not (is_valid_phone_number(number) and number not in get_spoofing()):
        await message.answer('❌ Send a valid number.', reply_markup=keyboard)
        return
    await state.update_data(number=number)

    await message.answer('🏢 Send service name.', reply_markup=keyboard)
    await state.set_state(callForm.waiting_for_service)
    
async def waiting_for_service_state(message:Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return

    service_name = message.text
    await state.update_data(service_name=service_name)

    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel call", "callback_data": "start_back"}]
        ]
    }
    await message.answer('👤 Send victim name.', reply_markup=keyboard)
    await state.set_state(callForm.waiting_for_name)

async def waiting_for_name_state(message:Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ confirm", "callback_data": "start_call"}],
            [{"text": "❌ Cancel call", "callback_data": "start_back"}]
        ]
    }
    await message.answer('✅ Press confirm bellow to start the call.', reply_markup=keyboard)
    
    victim_name = message.text
    await state.update_data(victim_name=victim_name)
    await state.set_state(callForm.waiting_for_confirmation)

async def waiting_for_confirmation_state(message:Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    victim_name = message.text
    await state.update_data(victim_name=victim_name)
    await state.set_state(callForm.waiting_for_confirmation)

async def start_call_state(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    data = await state.get_data()
    parts = ['/call',data.get('number'),data.get('service_name'),data.get('victim_name'),'6']
    await call_proccess(callback.message, parts, user_id, data.get('script'))
    await state.clear()


