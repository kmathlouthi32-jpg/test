from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from utils import escape_markdown_user, escape_markdown_text, fast_translate,escape_markdown_user, get_keyboard, preload_language_keyboard, add_user_fast, escape_markdown, get_user_cached, is_new_user, render_message, render_message, preload_language, is_lang_exist
from config import get_admin, get_groups, get_proof, get_video

async def start_command(message: Message, bot:Bot):
    user_id = message.from_user.id
    name = escape_markdown_user(message.from_user.first_name)
    new,users_count = is_new_user(user_id)
    if new:
        if message.from_user.username:
            username = escape_markdown_text("@"+message.from_user.username)
        else:
            username = 'N/A'
        await bot.send_message(chat_id=get_groups()['new_users_ID'],text=fr'''🆕 *New user*: {users_count}
*Username*\: {username}
*Name*\: `{name}`
*User ID*\: `{str(user_id)}`''',parse_mode='MarkdownV2')
        await add_user_fast(user_id)
    user_data = get_user_cached(user_id)
    if not(user_data['banned']):
        lang = message.from_user.language_code or "en"
        lang = lang.split("-")[0]
        if is_lang_exist(lang) or lang == 'en':
            keyboard = get_keyboard('start_keyboard',lang,channel_link=get_groups()["main_channel_link"],admin_link=get_admin()['link'],vouches_link=get_groups()["vouches_LINK"])
            text = render_message('start_message',lang,name=name)
            await message.answer_video(get_video(),caption=text,reply_markup=keyboard,parse_mode='MarkdownV2')
            return
        await message.answer(await fast_translate('🌍 Preparing your language, this will take a moment…',lang))
        await preload_language(lang)
        await preload_language_keyboard(lang)
        try:
            keyboard = get_keyboard('start_keyboard',lang,channel_link=get_groups()["main_channel_link"],admin_link=get_admin()['link'],vouches_link=get_groups()["vouches_LINK"])
            text = render_message('start_message',lang,name=name)
            await message.answer_video(get_video(),caption=text,reply_markup=keyboard,parse_mode='MarkdownV2')
        except Exception as e:
            await message.answer_video(get_video(),caption=text,reply_markup=keyboard)
            await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the start message\n{e}')

async def start_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if not(user_data['banned']):
        name = escape_markdown_user(callback.from_user.first_name)
        if callback.data == 'back1':
            try:
                await callback.message.delete()
            except:
                pass
        elif callback.data == 'back4':
            try:
                for i in range(6):
                    await bot.delete_message(user_id,callback.message.message_id-i)
            except:
                pass
        else:
            try:
                for i in range(2):
                    await bot.delete_message(user_id,callback.message.message_id-i)
            except:
                pass
        lang = callback.from_user.language_code or "en"
        lang = lang.split("-")[0]
        try:
            keyboard = get_keyboard('start_keyboard',lang,channel_link=get_groups()["main_channel_link"],admin_link=get_admin()['link'],vouches_link=get_groups()["vouches_LINK"])
            text = render_message('start_message', lang, name=name)
            await callback.message.answer_video(get_video(),caption=text,reply_markup=keyboard,parse_mode='MarkdownV2')
        except Exception as e:
            await callback.message.answer_video(get_video(),caption=text, reply_markup=keyboard)
            await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the start message\n{e}')

async def proofs_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer_video(get_proof()[0])
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard = get_keyboard('subback_keyboard',lang,back='back3')
        text = render_message('proofs_message',lang)
        await callback.message.answer_video(get_proof()[1],caption=text, reply_markup=keyboard,parse_mode='MarkdownV2')
    except Exception as e:
        await callback.message.answer_video(get_proof()[1],caption=text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the proofs message.\n{str(e)}')
    
async def help_command(message: Message, bot: Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard = get_keyboard('back_keyboard', lang, back='back1')
        text = render_message('help_message',lang)
        await message.answer(text, reply_markup=keyboard,parse_mode='MarkdownV2')
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the help message\n{str(e)}')

async def help_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    try:
        await callback.message.delete()
    except:
        pass
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard = get_keyboard('back_keyboard', lang,back='back1')
        text = render_message('help_message',lang)
        await callback.message.answer(text, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await callback.message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the help message\n{str(e)}')

async def features_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:return
    try:
        await callback.message.delete()
    except:
        pass
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard= get_keyboard('back_keyboard',lang,back='back1')
        text = render_message('features_message',lang)
        await callback.message.answer_video(get_video(),caption=text, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await callback.message.answer_video(get_video(),caption=text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the features message\n{str(e)}')





