import asyncio
import traceback
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import ErrorEvent
from aiogram.filters import CommandStart
from aiogram import F

from utils import (
    db,
    load_all_users,
    reload_users_every_12h,
)
from handlers import *
from config import get_admin

# ================== CONFIG ==================

BOT_TOKEN = "7886245319:AAGP1f1WQ_1Baw5ewNNlHTa6JsWRud5GP1Q"
ERROR_CHANNEL_ID = -1003771364465

#============================================

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = None
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
# GLOBAL ERROR HANDLER (AIROGRAM v3)
# ============================================

@dp.error()
async def global_error_handler(event: ErrorEvent):
    await report_error(event.exception, where="Aiogram Handler")

# ============================================
# COMMAND & CALLBACK REGISTRATION
# ============================================

# BASIC
dp.message.register(start_refferals_command, CommandStart(deep_link=True))
dp.message.register(start_command, Command("start"))

dp.callback_query.register(start_callback, F.data.startswith('start_back'))


# SUBSCRIPTIONS
dp.message.register(redeem_keys, Command("redeem"))

dp.callback_query.register(
    wallets_callback,
    F.data.in_(['sub:20','sub:50','sub:100','sub:250','sub:special_offer'])
)

dp.callback_query.register(
    wallet_callback,
    F.data.startswith('sub:20:') | F.data.startswith('sub:50:') | F.data.startswith('sub:100:') | F.data.startswith('sub:250:') | F.data.startswith('sub:special_offer:')
)

dp.callback_query.register(
    spoofing_wallets_callback,
    F.data.in_(['spoofing:50','spoofing:120','spoofing:240','spoofing:700'])
)

dp.callback_query.register(
    spoofing_wallet_callback,
    F.data.startswith('spoofing:50:') | F.data.startswith('spoofing:120:') | F.data.startswith('spoofing:240:') | F.data.startswith('sub:700:')
)

dp.callback_query.register(spoofing_callback, F.data == "spoof_packages")
dp.callback_query.register(subscriptions_callback, F.data == "subscriptions")
dp.callback_query.register(purchase_callback, F.data == "purchase")

# CALL  
dp.message.register(call_command,Command("call"))

dp.callback_query.register(recall_callback, F.data == 'recall')



# SETTINGS
dp.callback_query.register(waiting_for_script_state, F.data.startswith('call_script_'))
dp.message.register(waiting_for_number_state, callForm.waiting_for_number)
dp.message.register(waiting_for_service_state, callForm.waiting_for_service)
dp.message.register(waiting_for_name_state, callForm.waiting_for_name)
dp.message.register(waiting_for_confirmation_state, callForm.waiting_for_confirmation)
dp.callback_query.register(start_call_state, F.data == ('start_call'))

dp.message.register(ip_checking_message, Tools.ip_lookup)
dp.message.register(number_checking_message, Tools.number_lookup)
dp.message.register(email_checking_message, Tools.email_lookup)
dp.message.register(ai_chat_message, AIChat.chatting)
dp.message.register(process_my_AI_script, ScriptForm.waiting_for_discription)
dp.message.register(process_my_number, ScriptForm.waiting_for_number)
dp.message.register(script_name_handler, ScriptForm.waiting_for_name)
dp.message.register(script_greeting_handler, ScriptForm.waiting_for_greeting)
dp.message.register(script_code_handler, ScriptForm.waiting_for_code)
dp.message.register(script_goodbye_handler, ScriptForm.waiting_for_goodbye)


dp.callback_query.register(call_callback, F.data == ('makecall'))
dp.callback_query.register(ip_lookup_callback, F.data == ('ip_lookup'))
dp.callback_query.register(number_lookup_callback, F.data == ('number_info'))
dp.callback_query.register(email_lookup_proccess, F.data == ('email_lookup'))
dp.callback_query.register(tools_callback, F.data == ('tools'))
dp.callback_query.register(ask_ai_callback, F.data == ('aiassistant'))
dp.callback_query.register(earn_callback, F.data == ('earn'))
dp.callback_query.register(refresh_callback, F.data == ('refresh_leaderboard'))
dp.callback_query.register(leaderboard_callback, F.data == ('leaderboard'))
dp.callback_query.register(history_callback, F.data == ('history'))
dp.callback_query.register(lisen_script_callback, F.data.startswith('goodbye_') | F.data.startswith("greeting_"))
dp.callback_query.register(get_discription_callback, F.data == ('AI_generate_script'))
dp.callback_query.register(delete_script_callback, F.data.startswith('confirm_delete_'))
dp.callback_query.register(confirm_delete_scripts_callback, F.data.startswith('delete_script_'))
dp.callback_query.register(delete_scripts_callback, F.data == "delete_scripts")
dp.callback_query.register(manage_scripts_callback, F.data == "manage_custom_scripts")
dp.callback_query.register(view_one_custom_script_callback, F.data.startswith('view_custom_script_'))
dp.callback_query.register(caller_id_callback, F.data == "callerid")
dp.callback_query.register(my_number_callback, F.data == "mynumber")
dp.callback_query.register(script_name_callback, F.data == "manual_generate_script")
dp.callback_query.register(settings_callback, F.data.in_(["settings", 'settings_back']))
dp.callback_query.register(script_callback, F.data.in_(["script","scripts_list_back"]))
dp.callback_query.register(view_script_callback, F.data.in_(["scripts", "scripts_back"]))
dp.callback_query.register(language_callback, F.data == "language")
dp.callback_query.register(change_script_callback, F.data.startswith('script_') | F.data.startswith("script_custom_"))
dp.callback_query.register(change_lang_callback, F.data.startswith('lang_'))
dp.callback_query.register(view_one_script_callback, F.data.startswith('view_script_'))
dp.callback_query.register(set_script_callback, F.data.startswith('set_script_'))
dp.callback_query.register(create_script_callback, F.data == 'custom_script')

# ADMIN
dp.message.register(today_offer, Command("offer"))
dp.message.register(ban_command, Command("ban"))
dp.message.register(unban_command, Command("unban"))
dp.message.register(reload_command, Command("reload"))
dp.message.register(getwallet_command, Command("wallet"))
dp.message.register(switch_command, Command("switch"))
dp.message.register(send_all, Command("news"))
dp.message.register(keys_command, Command("keys"))
dp.message.register(generate_keys_command, Command("gkeys"))

dp.callback_query.register(keys_type_callback, F.data.in_(['spoofing', 'subscription']))

dp.callback_query.register(
    get_keys_callback,
    F.data.startswith('spoofing:') | F.data.startswith('subscription:')
)

# ============================================
# MAIN
# ============================================

async def main():
    print("🤖 Bot starting...")
    
    from aiogram.client.session.aiohttp import AiohttpSession
    global bot
    

    session = AiohttpSession(timeout=120)
    bot = Bot(token=BOT_TOKEN, session=session)

    try:
        await db.init_db()
        await db.create_tables()
        await load_all_users()

        asyncio.create_task(
            safe_task(reload_users_every_12h(), "User Reload")
        )

        admin = get_admin()
        await bot.send_message(admin["id"], "🟢 Bot online")

        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

    finally:
        print("🛑 Bot shutting down")
        await session.close()

if __name__ == "__main__":
    asyncio.run(main())

