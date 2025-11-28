from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import get_admin, get_groups
from utils import db, update_user_cache
from aiogram import Bot

def keys_type():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="2 Hours", callback_data="2 hours")],
        [InlineKeyboardButton(text="1 Day", callback_data="1 day"),
        InlineKeyboardButton(text="4 Days", callback_data="4 days")],
        [InlineKeyboardButton(text="1 Week", callback_data="1 week"),
        InlineKeyboardButton(text="1 Month", callback_data="1 month")],
        [InlineKeyboardButton(text="Lifetime", callback_data="lifetime")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]])

async def ban_command(message: Message, bot:Bot):
    if message.from_user.id != get_admin()['id']: return
    parts = message.text.split()
    if len(parts)<2: return
    await update_user_cache(int(parts[1]),'banned', True)
    await message.answer(f"User {parts[1]} banned from in the bot ✅")
    MAIN_CHANNELS = [get_groups()['main_channel_ID'],get_groups()['vouches_ID']]
    try:
        await bot.ban_chat_member(MAIN_CHANNELS[0], int(parts[1]))
    except Exception as e:
        message.answer(f"Failed to ban {int(parts[1])} in the main channel: {e}")
    try:
        await bot.ban_chat_member(MAIN_CHANNELS[1], int(parts[1]))
    except Exception as e:
        message.answer(f"Failed to ban {int(parts[1])} in the vouches channel: {e}")

async def unban_command(message: Message,bot:Bot):
    if message.from_user.id != get_admin()['id']: return
    parts = message.text.split()
    if len(parts)<2: return
    await update_user_cache(int(parts[1]),'banned', False)
    await message.answer(f"User {parts[1]} unbanned from the bot✅")
    MAIN_CHANNELS = [get_groups()['main_channel_ID'],get_groups()['vouches_ID']]
    try:
        await bot.unban_chat_member(MAIN_CHANNELS[0], int(parts[1]))
    except Exception as e:
        message.answer(f"Failed to unban {int(parts[1])} in the main channel: {e}")
    try:
        await bot.unban_chat_member(MAIN_CHANNELS[1], int(parts[1]))
    except Exception as e:
        message.answer(f"Failed to ubban {int(parts[1])} in the vouches channel: {e}")

async def keys_command(message: Message):
    if message.from_user.id != get_admin()['id']: return
    await message.answer("🔑 Select the keys type.",reply_markup=keys_type())

async def keys_callback(callback:CallbackQuery):
    if callback.from_user.id != get_admin()['id']: return
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("🔑 Select the keys type.",reply_markup=keys_type())

async def get_keys_callback(callback:CallbackQuery):
    if callback.from_user.id != get_admin()['id']: return
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("\n".join(await db.show_valid_keys(callback.data)),parse_mode='MarkdownV2')

async def generate_keys_callback(callback:CallbackQuery):
    if callback.from_user.id != get_admin()['id']: return
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("⏳ Generating keys...")
    await callback.message.answer(await db.generate_bulk_keys())

async def generate_keys_command(message: Message):
    if message.from_user.id != get_admin()['id']: return
    await message.answer("⏳ Generating keys...")
    await message.answer(await db.generate_bulk_keys())

