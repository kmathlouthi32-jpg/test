from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import get_admin, get_groups
from utils import db, update_user_cache, get_user_cached, get_all_users, load_all_users
from aiogram import Bot
import asyncio
from aiogram import types
from aiogram.exceptions import TelegramRetryAfter, TelegramAPIError

def get_wallet(x, crypto):
    wallets = [{
        'USDT': '`TY4Eh8RPdrhWSokWq9j9S4zVw7gd1Vrbaf`',
        'BTC': '`1KhvoitTrnopPqhxR1ayZ2ERw3d1g5BfdC`',
        'ETH': '`0x91ab56856eff7bc410fdac41c35a75d4e83410f6`',
        'SOL': '`GEPAmKTxPpM3mxYGze9CXmnSxAtZu1xQ9L9v7GEqmFts`',
        'LTC': '`LNFkiNNuqjLtY1vN4r3ihegnYfKmsc75Nm`'
    },
    {
        'USDT': '`TRRVAuPEGJ4EgE33u1pV6gNUXxM1R5v1aY`',
        'BTC': '`12g9D3pdhse6HSS38LYJr9bwXUGkeRbVHd`',
        'ETH': '`0xc76acc06684b2e2a2d43b9ba3b5f2618cd7a6307`',
        'SOL': '`8Ra9HKVrKNakEeQfqDzrVn1sFoQoFmbR51UHMRweT9hY`',
        'LTC': '`LRJ8n55djedy4jyKP3Kkqi6iEy3BYC1FLt`'
    }
    ]

    return wallets[x][crypto.upper()]

def keys_type():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="2 Hours", callback_data="2 hours")],
        [InlineKeyboardButton(text="1 Day", callback_data="1 day"),
        InlineKeyboardButton(text="4 Days", callback_data="4 days")],
        [InlineKeyboardButton(text="1 Week", callback_data="1 week"),
        InlineKeyboardButton(text="1 Month", callback_data="1 month")],
        [InlineKeyboardButton(text="Lifetime", callback_data="lifetime")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back1")]])

async def reload_command(message: Message):
    if message.from_user.id != get_admin()['id']: return
    await load_all_users()
    await message.answer("♻️ Reloaded all users!")

async def getwallet_command(message: Message):
    if message.from_user.id != get_admin()['id']: return
    parts = message.text.split()
    if len(parts)<3: return
    user_data = get_user_cached(int(parts[1]))
    await message.answer(get_wallet(user_data['wallet'],parts[2]),parse_mode='MarkdownV2')

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

async def switch_command(message: Message):
    if message.from_user.id != get_admin()['id']: return
    parts = message.text.split()
    if len(parts)<2: return
    user_data = get_user_cached(int(parts[1]))
    if user_data['wallet'] == 0:
        await update_user_cache(int(parts[1]),'wallet', 1)
        await message.answer(f"User {parts[1]} wallets switched✅")
        return
    await update_user_cache(int(parts[1]),'wallet', 0)
    await message.answer(f"User {parts[1]} wallets switched✅")

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

async def send_all(message: types.Message, bot: Bot):
    admin_id = get_admin().get('id')
    if message.from_user.id != admin_id:
        return

    # Get the text after the command
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("❌ Please provide a message to send.")
        return

    msg_to_send = parts[1]  # Keep multi-line text

    # Get all non-banned users
    user_ids = get_all_users()  # must be async

    sent = 0
    failed = 0
    try:
        await message.answer(msg_to_send, parse_mode='MarkdownV2')
        for user_id in user_ids:
            if user_id != get_admin()['id']:
                try:
                    await bot.send_message(user_id, msg_to_send, parse_mode='MarkdownV2')
                    sent += 1
                    await asyncio.sleep(0.05)  # Respect Telegram rate limits (~20 msg/sec)

                except TelegramRetryAfter as e:
                    print(str(e))
                    await asyncio.sleep(e.timeout)

                except TelegramAPIError as e:
                    error_text = str(e)
                    if "bot was blocked by the user" in error_text:
                        await message.answer(f"❌ User {user_id} blocked the bot. Skipping.")
                    elif "chat not found" in error_text:
                        await message.answer(f"❌ User {user_id} account deleted. ban.")
                        await update_user_cache(user_id, 'banned',True)
                    failed += 1

    except Exception as e:
        await message.answer(f"❌ Message entity problem.")
        failed += 1
        return

    await message.answer(f"✅ Sent: {sent}\n❌ Failed/blocked: {failed}")







