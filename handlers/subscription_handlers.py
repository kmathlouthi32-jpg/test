from aiogram.types import CallbackQuery
from utils import usd_to_crypto, escape_markdown_user, escape_markdown_text, db, get_user_cached, update_user_cache
from config import get_admin, get_groups
from datetime import datetime
from aiogram import Bot

async def purchase_proccess(callback):
    await callback.answer()
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "🎭 Spoof Packages",
        "callback_data": "spoof_packages"
      },
      {
        "text": "📦 Subscriptions ",
        "callback_data": "subscriptions"
      }
    ],
    [
      {
        "text": "⬅ Back",
        "callback_data": "start_back"
      }
    ]
  ]
}
    await callback.message.edit_text("""🛒 *Shop*

Choose a category:""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def subscriptions_proccess(callback):
    await callback.answer()
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "🥉 1 Day - $20",
        "callback_data": "sub:20"
      }
    ],
    [
      {
        "text": "🥈 3 Days - $50",
        "callback_data": "sub:50"
      }
    ],
    [
      {
        "text": "🥇 1 Week - $100",
        "callback_data": "sub:100"
      }
    ],
    [
      {
        "text": "💎 1 Month - $250",
        "callback_data": "sub:250"
      }
    ],
    [
      {
        "text": "🎁 SPECIAL OFFER",
        "callback_data": "sub:special_offer"
      }
    ],
    [
      {
        "text": "⬅ Back",
        "callback_data": "purchase"
      }
    ]
  ]
}
    await callback.message.edit_text("""📦 *Subscriptions*

✅ Unlimited calls during subscription
✅ No credit deduction
✅ Priority support

Select a plan:""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def wallets_proccess(callback):
    await callback.answer()
    price = callback.data
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "🔵 USDC",
        "callback_data": price+":usdc"
      }
    ,
      {
        "text": "🟨 BNB",
        "callback_data": price+":bnb"
      }
    ,
      {
        "text": "💎 TON",
        "callback_data": price+":ton"
      }
    ],
    [
      {
        "text": "🔷 XRP",
        "callback_data": price+":xrp"
      }
    ,
      {
        "text": "❤️ TRX",
        "callback_data": price+":trx"
      }
    ,
      {
        "text": "🥈 LTC",
        "callback_data": price+":ltc"
      }
    ],
    [
      {
        "text": "🌅 SOL",
        "callback_data": price+":sol"
      }
    ,
      {
        "text": "💎 ETH",
        "callback_data": price+":eth"
      }
    ,
      {
        "text": "💵 USDT",
        "callback_data": price+":usdt"
      }
    ],
    [
      {
        "text": "🟡 BTC",
        "callback_data": price+":btc"
      }
    ],
    [
      {
        "text": "⬅ Back",
        "callback_data": "subscriptions"
      }
    ]
  ]
}
    await callback.message.edit_text(r"""💸 *Pick a wallet to continue*\.
💬 _Other options available via Support_\.""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def wallet_proccess(callback, wallet_type):
    await callback.answer()
    text = callback.data[4:]
    symbol = text[text.find(':')+1:]
    symbol = symbol.upper()
    amount =  text[:text.find(':')]
    plans = {20: '1 Day Plan', 50: '3 Days Plan', 100: '1 Week Plan', 250: '1 Month Plan'}
    wallets = [{
        'USDT': ['TY4Eh8RPdrhWSokWq9j9S4zVw7gd1Vrbaf','TRON (TRC20)'],
        'BTC': ['1KhvoitTrnopPqhxR1ayZ2ERw3d1g5BfdC','BTC'],
        'ETH': ['0x91ab56856eff7bc410fdac41c35a75d4e83410f6','Ethereum (ERC20)'],
        'SOL': ['GEPAmKTxPpM3mxYGze9CXmnSxAtZu1xQ9L9v7GEqmFts','SOL'],
        'LTC': ['LNFkiNNuqjLtY1vN4r3ihegnYfKmsc75Nm','LTC'],
        'TRX': ['TY4Eh8RPdrhWSokWq9j9S4zVw7gd1Vrbaf','TRON (TRC20)'],
        'XRP': ['rNxp4h8apvRis6mJf9Sh8C6iRxfrDWN7AV','XRP Ledger'],
        'TON': ['UQDiP6R2XT8XnM_u36odBIA4J8S61RyMWnp9vfDCYgZ9ZIq4','TON'],
        'BNB': ['0x91ab56856eff7bc410fdac41c35a75d4e83410f6','BSC (BEP20)'],
        'USDC': ['0x91ab56856eff7bc410fdac41c35a75d4e83410f6','Ethereum (ERC20)']
    },
    {
        'USDT': ['THqWBtVxYRpWhgmMNd2M5nMkjTTVmsVgxh','TRON (TRC20)'],
        'BTC': ['1M6Q4pFzofeBvA9e2CQ9rhtLyLkLc34p3q','BTC'],
        'ETH': ['0x1c89c55def70cb0fccaf058abfc5a1e493d0e297','Ethereum (ERC20)'],
        'SOL': ['5bPVRzUqc4ThfNST9uaKMn8PoS3xip1JxRShb8PWwWFW','SOL'],
        'LTC': ['LMWe7aWQkBcQZT5fzhfPDvZMHdYg9rwuwp','LTC'],
        'TRX': ['THqWBtVxYRpWhgmMNd2M5nMkjTTVmsVgxh','TRON (TRC20)'],
        'XRP': ['rJn2zAPdFA193sixJwuFixRkYDUtx3apQh','XRP'],
        'TON': ['UQAWaH2rvahtHvyTduGsufRHgPT6BwjQXEb01zix2IsosO_T','TON'],
        'BNB': ['0x1c89c55def70cb0fccaf058abfc5a1e493d0e297','BSC (BEP20)'],
        'USDC': ['0x1c89c55def70cb0fccaf058abfc5a1e493d0e297','Ethereum (ERC20)'],
    }
    ]
    call = ''
    if amount == "special_offer":
        call = "special_offer"
        admin = get_user_cached(get_admin()['id'])
        full_offer = admin['offer']
        parts = full_offer.split('+')
        amount = int(parts[0])
        if parts[1] == '1':
          plan = '1 Day Plan'
        elif parts[1] == '3':
          plan= '3 Days Plan'  
        elif parts[1] == '7':
          plan = '1 Week Plan' 
        elif parts[1] == '30':
          plan = '1 Month Plan' 

        price = [k for k, v in plans.items() if v == plan][0]
        discount = str(((price - amount) / price) * 100)+"%"
        gift = f'{parts[2]} PayPal Logs & {parts[3]} CC'
    
    wallet = wallets[wallet_type].get(symbol, "N/A")[0]
    network = wallets[wallet_type].get(symbol, "N/A")[1]
    if call != "special_offer":
      plan = plans.get(int(amount), "Unknown Plan")
      discount = '0%'
      gift = '0 PayPal Logs & 0 CC'
    price = usd_to_crypto(symbol, int(amount))
    date = str(datetime.now())
    first = await callback.message.edit_text(fr"""ℹ️ Payment Details
━━━━━━━━━━━━━━━
🪙 *Currency*: {symbol.upper()}
💰 *Amount*: {escape_markdown_user(price)}
⏳ *Plan*: {escape_markdown_user(plan)}
💳 *Wallet*: `{escape_markdown_user(wallet)}`
🌐 *Network*: `{escape_markdown_user(network)}`
🎁 *Extra gift*: {escape_markdown_user(gift)}
🏷️ *Discount*: {escape_markdown_user(discount)}
📅 *Date*: {escape_markdown_user(date)}""", parse_mode='MarkdownV2')
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": f'start_back:{first.message_id}'
      }
    ]
  ]
}
    await callback.message.answer(fr'''🔐 *To complete your purchase*:
_Send the amount via the *{symbol}* wallet in *{escape_markdown_user(network)}* network and send a screenshot to [Support]({escape_markdown_user(get_admin()['link'])})\._''', parse_mode='MarkdownV2',disable_web_page_preview=True, reply_markup=keyboard)

async def spoofing_proccess(callback):
    await callback.answer()
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "🥉 1 Day - $50",
        "callback_data": "spoofing:50"
      }
    ],
    [
      {
        "text": "🥈 3 Days - $120",
        "callback_data": "spoofing:120"
      }
    ],
    [
      {
        "text": "🥇 1 Week - $240",
        "callback_data": "spoofing:240"
      }
    ],
    [
      {
        "text": "💎 1 Month - $700",
        "callback_data": "spoofing:700"
      }
    ],
    [
      {
        "text": "⬅ Back",
        "callback_data": "purchase"
      }
    ]
  ]
}
    await callback.message.edit_text("""🎭 *Spoof Packages*

✅ Dedicated spoof gateway
✅ Custom caller ID spoofing
✅ Premium routes

Select a package:""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def spoofing_wallets_proccess(callback):
    await callback.answer()
    price = callback.data
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "🔵 USDC",
        "callback_data": price+":usdc"
      }
    ,
      {
        "text": "🟨 BNB",
        "callback_data": price+":bnb"
      }
    ,
      {
        "text": "💎 TON",
        "callback_data": price+":ton"
      }
    ],
    [
      {
        "text": "🔷 XRP",
        "callback_data": price+":xrp"
      }
    ,
      {
        "text": "❤️ TRX",
        "callback_data": price+":trx"
      }
    ,
      {
        "text": "🥈 LTC",
        "callback_data": price+":ltc"
      }
    ],
    [
      {
        "text": "🌅 SOL",
        "callback_data": price+":sol"
      }
    ,
      {
        "text": "💎 ETH",
        "callback_data": price+":eth"
      }
    ,
      {
        "text": "💵 USDT",
        "callback_data": price+":usdt"
      }
    ],
    [
      {
        "text": "🟡 BTC",
        "callback_data": price+":btc"
      }
    ],
    [
      {
        "text": "⬅ Back",
        "callback_data": "spoof_packages"
      }
    ]
  ]
}
    await callback.message.edit_text(r"""💸 *Pick a wallet to continue*\.
💬 _Other options available via Support_\.""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def spoofing_wallet_proccess(callback, wallet_type):
    await callback.answer()
    text = callback.data[9:]
    symbol = text[text.find(':')+1:]
    symbol = symbol.upper()
    amount =  text[:text.find(':')]
    plans = {50: '1 Day Spoofing Plan', 120: '3 Days Spoofing Plan', 240: '1 Week Spoofing Plan', 700: '1 Month Spoofing Plan'}
    wallets = [{
        'USDT': ['TY4Eh8RPdrhWSokWq9j9S4zVw7gd1Vrbaf','TRON (TRC20)'],
        'BTC': ['1KhvoitTrnopPqhxR1ayZ2ERw3d1g5BfdC','BTC'],
        'ETH': ['0x91ab56856eff7bc410fdac41c35a75d4e83410f6','Ethereum (ERC20)'],
        'SOL': ['GEPAmKTxPpM3mxYGze9CXmnSxAtZu1xQ9L9v7GEqmFts','SOL'],
        'LTC': ['LNFkiNNuqjLtY1vN4r3ihegnYfKmsc75Nm','LTC'],
        'TRX': ['TY4Eh8RPdrhWSokWq9j9S4zVw7gd1Vrbaf','TRON (TRC20)'],
        'XRP': ['rNxp4h8apvRis6mJf9Sh8C6iRxfrDWN7AV','XRP Ledger'],
        'TON': ['UQDiP6R2XT8XnM_u36odBIA4J8S61RyMWnp9vfDCYgZ9ZIq4','TON'],
        'BNB': ['0x91ab56856eff7bc410fdac41c35a75d4e83410f6','BSC (BEP20)'],
        'USDC': ['0x91ab56856eff7bc410fdac41c35a75d4e83410f6','Ethereum (ERC20)']
    },
    {
        'USDT': ['THqWBtVxYRpWhgmMNd2M5nMkjTTVmsVgxh','TRON (TRC20)'],
        'BTC': ['1M6Q4pFzofeBvA9e2CQ9rhtLyLkLc34p3q','BTC'],
        'ETH': ['0x1c89c55def70cb0fccaf058abfc5a1e493d0e297','Ethereum (ERC20)'],
        'SOL': ['5bPVRzUqc4ThfNST9uaKMn8PoS3xip1JxRShb8PWwWFW','SOL'],
        'LTC': ['LMWe7aWQkBcQZT5fzhfPDvZMHdYg9rwuwp','LTC'],
        'TRX': ['THqWBtVxYRpWhgmMNd2M5nMkjTTVmsVgxh','TRON (TRC20)'],
        'XRP': ['rJn2zAPdFA193sixJwuFixRkYDUtx3apQh','XRP'],
        'TON': ['UQAWaH2rvahtHvyTduGsufRHgPT6BwjQXEb01zix2IsosO_T','TON'],
        'BNB': ['0x1c89c55def70cb0fccaf058abfc5a1e493d0e297','BSC (BEP20)'],
        'USDC': ['0x1c89c55def70cb0fccaf058abfc5a1e493d0e297','Ethereum (ERC20)'],
    }
    ]
    
    wallet = wallets[wallet_type].get(symbol, "N/A")[0]
    network = wallets[wallet_type].get(symbol, "N/A")[1]
    plan = plans.get(int(amount), "Unknown Plan")
    price = usd_to_crypto(symbol, int(amount))
    date = str(datetime.now())

    first = await callback.message.edit_text(fr"""ℹ️ Payment Details
━━━━━━━━━━━━━━━
🪙 *Currency*: {symbol.upper()}
💰 *Amount*: {escape_markdown_user(price)}
⏳ *Plan*: {escape_markdown_user(plan)}
💳 *Wallet*: `{escape_markdown_user(wallet)}`
🌐 *Network*: `{escape_markdown_user(network)}`
📅 *Date*: {escape_markdown_user(date)}""", parse_mode='MarkdownV2')
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": f'start_back:{first.message_id}'
      }
    ]
  ]
}
    await callback.message.answer(fr'''🔐 *To complete your purchase*:
_Send the amount via the *{symbol}* wallet in *{escape_markdown_user(network)}* network and send a screenshot to [Support]({escape_markdown_user(get_admin()['link'])})\._''', parse_mode='MarkdownV2',disable_web_page_preview=True, reply_markup=keyboard)



async def purchase_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    await purchase_proccess(callback)

async def subscriptions_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    await subscriptions_proccess(callback)

async def wallets_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    await wallets_proccess(callback)

async def redeem_keys(message, bot:Bot):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']: return
    parts = message.text.split()
    if len(parts)<2:
        await message.answer('Usage: /redeem <key>')
        return
    duration_text,expiry,plan_type = await db.redeem_key(parts[1], user_data['expiry_date'])

    if duration_text == 'wrong_key':
        await message.answer('❌ Invalid key.')
        return
    if duration_text == 'used_key':
        await message.answer('❌ Key already used.')
        return

    else:
        text = fr"""✅ *{plan_type} Key Redeemed Successfully*\!
  
🕐 *Plan*: {duration_text}
🚀 _You can now use Dragon OTP_\!"""
        await message.answer(text,parse_mode='MarkdownV2')
        if plan_type == 'subscription':
          await update_user_cache(user_id, 'expiry_date', str(expiry))
        else:
           await update_user_cache(user_id, 'spoof', str(expiry)) 

    if message.from_user.username:
        username = "@"+message.from_user.username
    else:
        username = 'N/A'
    name = message.from_user.first_name
    
    await bot.send_message(chat_id=get_groups()['redeemed_keys_ID'],text=fr'''*{plan_type} Key For {duration_text}*
Redeemed by {escape_markdown_text(username)}
Name: `{escape_markdown_text(name)}`
Chat Id: `{user_id}`
Key: `{parts[1]}`''',parse_mode='MarkdownV2')

async def wallet_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    wallet_type = user_data['wallet']
    await wallet_proccess(callback, wallet_type)

async def spoofing_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    await spoofing_proccess(callback)

async def spoofing_wallets_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    await spoofing_wallets_proccess(callback)

async def spoofing_wallet_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned'] == True: return
    wallet_type = user_data['wallet']
    await spoofing_wallet_proccess(callback, wallet_type)
    


