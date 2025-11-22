from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from utils import init_db, create_tables, escape_markdown
from handlers import *
from time import sleep

bot = Bot(token='7886245319:AAGP1f1WQ_1Baw5ewNNlHTa6JsWRud5GP1Q')
dp = Dispatcher()



# START / HELP / UNKNOWN
# COMMAND
dp.message.register(help_command, Command(commands=["help"]))
dp.message.register(start_command, Command(commands=["start"]))

# CALLBACK
dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(start_callback,
                           lambda c: c.data in ['back1', 'back4'])

# SUBSCRIPTION
# COMMANDS
dp.message.register(purchase_command, Command(commands=["purchase"]))
dp.message.register(my_profile_command, Command(commands=["plan"]))
dp.message.register(redeem_keys, Command(commands=["redeem"]))

# CALLBACKS
dp.callback_query.register(wallets_callback,
                           lambda c: c.data in ['20', '50', '90', '200'])
dp.callback_query.register(wallet_callback, lambda c: ':' in c.data)
dp.callback_query.register(purchase_callback, lambda c: c.data == "purchase")
dp.callback_query.register(my_profile_callback, lambda c: c.data == "plan")

# CALL
dp.message.register(
    call_command,
    Command(commands=[
        'repcall', 'recall', "call", "paypal", "venmo", "applepay", "coinbase",
        "microsoft", "amazon", "quadpay", "cashapp", "citizens", "marcus",
        "carrier", 'creditcard'
    ]))
dp.message.register(Phonelist_commands, Command(commands=["phonelist"]))

# CALLBACKS
dp.callback_query.register(otp_accept_callback, lambda c: c.data == "acp")

# STTINGS
# COMMANDS
dp.message.register(voicelist_command,
                    Command(commands=["voicelist"]))  # NEED WORK
dp.message.register(setvoice_command, Command(commands=["setvoice"]))
dp.message.register(setscript_command, Command(commands=["setscript"]))
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
dp.message.register(keys_command, Command(commands=["keys"]))
dp.message.register(generate_keys_command, Command(commands=["gkeys"]))

# CALLBACKS
dp.callback_query.register(keys_callback, lambda c: c.data == 'keys')
dp.callback_query.register(generate_keys_callback,
                           lambda c: c.data == 'g_keys')
dp.callback_query.register(
    get_keys_callback,
    lambda c: c.data in ['2 hours', '1 day', '4 days', '1 week', '1 month'])

dp.message.register(
    unknown_command,
    lambda message: message.text and message.text.startswith('/'))


async def main():
    print("Bot is running...")
    await init_db()
    await create_tables()
    await dp.start_polling(bot)


while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        sleep(3)




