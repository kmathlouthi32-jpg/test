from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from utils import init_db, create_tables, escape_markdown, keep_alive

from handlers import *

bot = Bot(token='8276206384:AAGH6-LHRyqhZixP28Kum-VYRthyZqQgKJ4')
dp = Dispatcher()

keep_alive()

import psutil, os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    return round(mem, 2)

# Example: log it every few minutes
async def log_memory():
    while True:
        await bot.send_message(-1002942544591,text=f"💾 Memory usage: *{escape_markdown(str(get_memory_usage()))}* MB",parse_mode='MarkdownV2')
        await asyncio.sleep(300)


# START / HELP / UNKNOWN
# COMMAND
dp.message.register(help_command, Command(commands=["help"]))
dp.message.register(start_command, Command(commands=["start"]))

# CALLBACK
dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(start_callback, lambda c: c.data in ['back1','back4'])

# SUBSCRIPTION
# COMMANDS
dp.message.register(purchase_command, Command(commands=["purchase"]))
dp.message.register(my_profile_command, Command(commands=["plan"]))
dp.message.register(redeem_keys, Command(commands=["redeem"]))

# CALLBACKS
dp.callback_query.register(wallets_callback, lambda c: c.data in ['20','50','90','200'])
dp.callback_query.register(wallet_callback, lambda c: ':' in c.data)
dp.callback_query.register(purchase_callback, lambda c: c.data == "purchase")
dp.callback_query.register(my_profile_callback, lambda c: c.data == "plan")


# CALL 
dp.message.register(call_command, Command(commands=['recall',"call","paypal", "venmo", "applepay", "coinbase", "microsoft", "amazon", "quadpay", "cashapp", "citizens", "marcus", "carrier",'creditcard']))
dp.message.register(Phonelist_commands, Command(commands=["phonelist"]))

# CALLBACKS
dp.callback_query.register(otp_accept_callback, lambda c: c.data == "acp")

# STTINGS
# COMMANDS
dp.message.register(voicelist_command, Command(commands=["voicelist"]))  # NEED WORK
dp.message.register(setvoice_command, Command(commands=["setvoice"]))
dp.message.register(setscript_command, Command(commands=["setscript"]))
dp.message.register(process_script_text, ScriptForm.waiting_for_script)
dp.message.register(view_script, Command(commands=["script"]))

# CALLBACK
dp.callback_query.register(changevoice_callback, lambda c: c.data in ['Michael','Ethan','Mark','Mia','Sofia','Andria'])

# ADMIN
# COMMANDS
dp.message.register(ban_command, Command(commands=["ban"]))
dp.message.register(unban_command, Command(commands=["unban"]))
dp.message.register(keys_command, Command(commands=["keys"]))

# CALLBACKS
dp.callback_query.register(keys_callback, lambda c: c.data=='keys')
dp.callback_query.register(get_keys_callback, lambda c: c.data in ['2 hours','1 day','4 days','1 week','1 month'])

dp.message.register(unknown_command,lambda message: message.text and message.text.startswith('/'))

async def main():
    print("Bot is running...")
    await init_db()
    await create_tables()
    asyncio.create_task(log_memory())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

