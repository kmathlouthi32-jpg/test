from aiogram.types import Message
from aiogram import types, Bot
from config import get_voices, get_admin
from utils import get_keyboard, get_user_cached, update_user_cache, get_message, render_message
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

async def voicelist_command(message: Message):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    keyboard = get_keyboard('back_keyboard',lang,back='back4')
    names = ['👨 Michael', '👩 Andria' ,' 👨 Ethan', '👩 Sofia' ,' 👨 Mark',' 👩 Mia']
    for i in range(5):
        await message.answer_audio(get_voices()[i],caption=names[i])
    await message.answer_audio(get_voices()[5],caption=names[5],reply_markup=keyboard)

async def setvoice_command(message: Message, bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    current_voice = user_data['voice']
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    if current_voice in ['Michael','Ethan','Mark']:
        text = render_message('setvoicem_message',lang, current_voice=current_voice)
    else:
        text = render_message('setvoicef_message',lang, current_voice=current_voice)
    keyboard = get_keyboard('voices_keyboard',lang)
    try:
        await message.answer(text ,reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await message.answer(text ,reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the setvoice message\n{e}')

async def changevoice_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    selected_voice = callback.data
    current_voice = user_data['voice']
    await callback.message.delete()
    if current_voice == selected_voice:
        text = get_message('voiceused_message',lang)
        await callback.message.answer(text)
        return
    await update_user_cache(user_id, 'voice',selected_voice)
    text = get_message('voicechanged_message',lang)
    await callback.message.answer(text)

# --- STATE DEFINITION ---
class ScriptForm(StatesGroup):
    waiting_for_script = State()


# --- COMMAND HANDLER ---
async def setscript_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    text = get_message('scriptreq_message',lang)
    await message.answer(text)
    await state.set_state(ScriptForm.waiting_for_script)


# --- MESSAGE HANDLER FOR USER REPLY ---
async def process_script_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    script_text = message.text.strip()
    lang=message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    # ✅ Example: Save to your database
    await update_user_cache(user_id, 'custom_script',script_text)
    text = get_message('scriptset_message',lang)
    await message.answer(text)
    await state.clear()  # reset FSM state

async def view_script(message: Message, bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    script = user_data['custom_script']
    lang=message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    if script!='N/A':
        msg = render_message('script_message',lang,script=script)
    else:
        msg = render_message('noscript_message',lang)
    try:
        await message.answer(msg, parse_mode='MarkdownV2')
    except Exception as e:
        await message.answer(msg)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the script message\n{e}')
