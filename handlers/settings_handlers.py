from aiogram.types import Message
from aiogram import types
from config import get_voices
from utils import escape_markdown, get_user_cached, update_user_cache
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

def get_setvoice_message(current_voice):
    if current_voice in ['Michael','Ethan','Mark']:
        gender = 'Male'
    else:
        gender = 'Female'
    return fr"""🎙 *Voice Settings*

🗣 *Current Voice:* `[{current_voice}]`  
⚥ *Gender:* `[{gender}]`

To change your voice, select *A Voice* below\.  
For a full list of available voices, use: `/voicelist`

🛠 Personalize your voice for a better and more natural experience\."""

def setvoice_keyboard():
    return  InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚹 Michael", callback_data="Michael"),
        InlineKeyboardButton(text="🚺 Andria", callback_data="Andria")
    ],
    [
        InlineKeyboardButton(text="🚹 Ethan", callback_data="Ethan"),
        InlineKeyboardButton(text="🚺 Sofia", callback_data="Sofia")
    ],
    [
        InlineKeyboardButton(text="🚹 Mark", callback_data="Mark"),
        InlineKeyboardButton(text="🚺 Mia", callback_data="Mia")
    ],
    [
        InlineKeyboardButton(text="🔙 Keep Current Voice", callback_data="back1")
    ]
])

async def voicelist_command(message: Message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back4")]
    ])
    names = ['👨 Michael', '👩 Andria' ,' 👨Ethan', '👩 Sofia' ,' 👨 Mark',' 👩 Mia']
    for i in range(5):
        await message.answer_audio(get_voices()[i],caption=names[i])
    await message.answer_audio(get_voices()[5],caption=names[5],reply_markup=keyboard)

async def setvoice_command(message: Message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    current_voice = user_data['voice']
    await message.answer(get_setvoice_message(current_voice),reply_markup=setvoice_keyboard(), parse_mode='MarkdownV2')

async def changevoice_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']: return
    selected_voice = callback.data
    current_voice = user_data['voice']
    await callback.message.delete()
    if current_voice == selected_voice:
        await callback.message.answer("🎧 Voice already in use.")
        return
    await update_user_cache(user_id, 'voice',selected_voice)
    await callback.message.answer('✅ Voice updated.')

# --- STATE DEFINITION ---
class ScriptForm(StatesGroup):
    waiting_for_script = State()


# --- COMMAND HANDLER ---
async def setscript_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:
        return
    await message.answer("📝 Please send me your custom script text:")
    await state.set_state(ScriptForm.waiting_for_script)


# --- MESSAGE HANDLER FOR USER REPLY ---
async def process_script_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    script_text = message.text.strip()

    # ✅ Example: Save to your database
    await update_user_cache(user_id, 'custom_script',script_text)

    await message.answer("✅ Your custom script has been saved successfully.")
    await state.clear()  # reset FSM state

async def view_script(message: Message):
    user_id = message.from_user.id
    user_data = await get_user_cached(user_id)
    if user_data['banned']:return
    script = user_data['custom_script']
    if script!='N/A':
        msg = rf"""*Your current script*:
{escape_markdown(script)}"""
    else:
        msg = escape_markdown("No script set.")
    await message.answer(msg,parse_mode='MarkdownV2')
