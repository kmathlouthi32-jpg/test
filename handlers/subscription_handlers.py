from aiogram.types import CallbackQuery
from utils import get_keyboard,fast_translate,escape_markdown_text, check_subscription, get_wallet_message, db, get_user_cached, update_user_cache, get_message, render_message
from config import get_admin, get_groups
from datetime import datetime
from aiogram import Bot

async def purchase_command(message,bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]

    try:
        keyboard = get_keyboard('pricing_keyboard',lang)
        text = render_message('pricing_message',lang)
        await message.answer(text, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the pricing message\n{str(e)}')

async def purchase_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    try:
        await callback.message.delete()
    except:
        pass
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard = get_keyboard('pricing_keyboard',lang)
        text = render_message('pricing_message',lang)
        await callback.message.answer(text, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await callback.message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the pricing message\n{str(e)}')

async def wallets_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    price = callback.data
    try:
        await callback.message.delete()
    except:
        pass
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard = get_keyboard('wallets_keyboard',lang,admin_link=get_admin()['link'],price=price)
        text = render_message('wallets_message',lang)
        await callback.message.answer(text, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await callback.message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the wallets message\n{str(e)}')

async def my_profile_command(message, bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    if check_subscription(user_data['expiry_date']) == True:
        expiry_date = user_data['expiry_date']
        expiry_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
        days_left = str(expiry_date-datetime.now())
        days_left = days_left[:days_left.find(',')]
        if lang != 'en':
            days_left = await fast_translate(days_left, lang)
        try:
            keyboard = get_keyboard('back_keyboard',lang,back='back1')
            text = render_message('plan_message',lang , days_left=days_left)
            await message.answer(text, reply_markup=keyboard,parse_mode='MarkdownV2')
        except Exception as e:
            await message.answer(text, reply_markup=keyboard)
            await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the plan message\n{str(e)}')
        return
    try:
        keyboard = get_keyboard('subback_keyboard',lang,back='back1')
        text = render_message('noplan_message',lang)
        await message.answer(text, reply_markup=keyboard)
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the start message\n{str(e)}')

async def redeem_keys(message, bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    parts = message.text.split()
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    if len(parts)<2:
        text = get_message('nokey_message',lang)
        await message.answer(text)
        return
    duration_text,expiry = await db.redeem_key(user_id, parts[1], user_data['expiry_date'], user_data['rep'])
    if duration_text == 'norep':
        text = get_message('norep_message',lang)
        await message.answer(text)
        return
    if duration_text == 'wrong_key':
        text = get_message('wrongkey_message',lang)
        await message.answer(text)
        return
    if duration_text == 'used_key':
        text = get_message('usedkey_message',lang)
        await message.answer(text)
        return
    if duration_text in ['norep','wrongkey','usedkey']:return
    else:
        if duration_text=='Repport Calls':
            text = get_message('repportkey_message',lang)
            await message.answer(text)
            await update_user_cache(user_id, 'rep', True)
        else:
            text = render_message('redeemkey_message',lang,label=duration_text)
            await message.answer(text,parse_mode='MarkdownV2')
            await update_user_cache(user_id, 'expiry_date', str(expiry))
    if message.from_user.username:
        username = "@"+message.from_user.username
    else:
        username = 'N/A'
    name = message.from_user.first_name
    
    await bot.send_message(chat_id=get_groups()['redeemed_keys_ID'],text=fr'''*Key For {duration_text}*
Redeemed by {escape_markdown_text(username)}
Name: `{escape_markdown_text(name)}`
Chat Id: `{user_id}`
Key: `{parts[1]}`''',parse_mode='MarkdownV2')

async def wallet_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    price_symbol = callback.data
    amount = price_symbol[:price_symbol.find(':')]
    symbol = price_symbol[price_symbol.find(':')+1:]
    lang = callback.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        await callback.message.delete()
    except:
        pass
    try:
        text = get_wallet_message(symbol,float(amount),user_data['wallet'],lang)
        await callback.message.answer(text, parse_mode='MarkdownV2',disable_web_page_preview=True)
    except Exception as e:
        await callback.message.answer(text,disable_web_page_preview=True)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the wallet_message\n{str(e)}')

async def prices_command(message, bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    lang = message.from_user.language_code or "en"
    lang = lang.split("-")[0]
    try:
        keyboard = get_keyboard('subback_keyboard',lang,back='back1')
        text = render_message('prices_message',lang)
        await message.answer(text, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)
        await bot.send_message(get_admin()['id'],f'⚠ problem in {lang} Language in the prices_message\n{str(e)}')


