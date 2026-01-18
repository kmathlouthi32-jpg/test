from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
import psutil
import os
from utils import db, load_all_users, load_messages,reload_users_every_12h
from handlers import *
from time import sleep
from utils import load_keyboards

asyncio.set_event_loop(asyncio.new_event_loop())

def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    return round(mem, 2)

# Example: log it every few minutes
async def log_memory():
    while True:
        await bot.send_message(-1002942544591,text=f"💾 Memory usage: {str(get_memory_usage())} MB")
        await asyncio.sleep(300)

bot = Bot(token='7886245319:AAGP1f1WQ_1Baw5ewNNlHTa6JsWRud5GP1Q')
dp = Dispatcher(skip_updates=True)

# START / HELP / UNKNOWN
# COMMAND
dp.message.register(help_command, Command(commands=["help"]))
dp.message.register(start_command, Command(commands=["start"]))

# CALLBACK
dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(proofs_callback, lambda c: c.data == "proofs")
dp.callback_query.register(features_callback, lambda c: c.data == "features")
dp.callback_query.register(start_callback,
                           lambda c: c.data in ['back1', 'back4','back3'])

# SUBSCRIPTION
# COMMANDS
dp.message.register(purchase_command, Command(commands=["purchase"]))
dp.message.register(prices_command, Command(commands=["prices"]))
dp.message.register(my_profile_command, Command(commands=["plan"]))
dp.message.register(redeem_keys, Command(commands=["redeem"]))

# CALLBACKS
dp.callback_query.register(wallets_callback,
                           lambda c: c.data in ['15','20', '50', '90', '200','1000'])
dp.callback_query.register(wallet_callback, lambda c: ':' in c.data)
dp.callback_query.register(purchase_callback, lambda c: c.data == "purchase")

# CALL
dp.message.register(
    call_command,
    Command(commands=[
        'repportcall', 'recall', "call", "paypal", "venmo", "applepay", "coinbase",
        "microsoft", "amazon", "quadpay", "cashapp", "citizens", "marcus",
        "carrier", 'creditcard','ssn','customcall','customvoice'
    ]))
dp.message.register(Phonelist_commands, Command(commands=["phonelist"]))

# CALLBACKS
dp.callback_query.register(otp_accept_callback, lambda c: c.data in ["acp",'den','card','cvv','rout'])

# STTINGS
# COMMANDS
dp.message.register(voicelist_command,
                    Command(commands=["voicelist"]))  # NEED WORK
dp.message.register(setvoice_command, Command(commands=["setvoice"]))
dp.message.register(setscript_command, Command(commands=["createscript"]))
dp.message.register(process_script_text, ScriptForm.waiting_for_script)
dp.message.register(view_script, Command(commands=["script"]))

# CALLBACK
dp.callback_query.register(
    changevoice_callback,
    lambda c: c.data in ['Michael', 'Ethan', 'Mark', 'Mia', 'Sofia', 'Andria'])

# ADMIN
# COMMANDS
dp.message.register(ban_command, Command(commands=["ban"]))
dp.message.register(unban_command, Command(commands=["unban"]))
dp.message.register(reload_command, Command(commands=["reload"]))
dp.message.register(getwallet_command, Command(commands=["wallet"]))
dp.message.register(switch_command, Command(commands=["switch"]))
dp.message.register(send_all, Command(commands=["news"]))
dp.message.register(keys_command, Command(commands=["keys"]))
dp.message.register(generate_keys_command, Command(commands=["gkeys"]))

# CALLBACKS
dp.callback_query.register(keys_callback, lambda c: c.data == 'keys')
dp.callback_query.register(generate_keys_callback,
                           lambda c: c.data == 'g_keys')
dp.callback_query.register(
    get_keys_callback,
    lambda c: c.data in ['2 hours', '1 day', '4 days', '1 week', '1 month', 'lifetime'])





async def main():
    print("🤖 Bot is running...")
    await db.init_db()
    await db.create_tables()
    await load_all_users()
    await load_messages()
    await load_keyboards()
    asyncio.create_task(log_memory())
    asyncio.create_task(reload_users_every_12h())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())

















