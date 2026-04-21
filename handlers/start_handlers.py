from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from utils import check_subscription, escape_markdown_user, get_user_cached, is_new_user, add_user_fast, update_user_cache
from config import get_groups, get_video, get_admin
from datetime import datetime
from aiogram.fsm.context import FSMContext


async def start_proccess(msg, username, expiry_date):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "📞 Make a Call",
        "callback_data": "makecall"
      },
      {
        "text": "💳 Purchase",
        "callback_data": "purchase"
      }
    ],
    [
      {
        "text": "⚙️ settings",
        "callback_data": "settings"
      },
      {
        "text": "📓 History",
        "callback_data": "history"
      }
    ],
    [
      {
        "text": "🧰 Tools",
        "callback_data": "tools"
      },
      {
        "text": "🤖 AI Assitant",
        "callback_data": "aiassistant"
      }
    ],
    [
      {
        "text": "🎁 Earn",
        "callback_data": "earn"
      },
      {
        "text": "🏆 Leaderboard",
        "callback_data": "leaderboard"
      }
    ],
    [
      {
        "text": "📣 Channel",
        "url": get_groups()['main_channel_link']
      },
      {
        "text": "✅ Vouches",
        "url": get_groups()['vouches_LINK']
      }
    ]
  ]
}
    if not(check_subscription(expiry_date)) or expiry_date== 'N/A':
        rest_calls = '0 • 0 min available'
        plan = 'No subscription'
    else:
        rest_calls = f"calls end in {escape_markdown_user(expiry_date[0:expiry_date.find(' ')])}"
        plan = 'Premium'
    if expiry_date != 'N/A':
      expiry_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
      days_left = str(expiry_date-datetime.now())
      days_left = days_left[:days_left.find(',')]
    else:
        days_left = "0 Days"
    message = fr'''🐲 *DRAGON OTP* 👑
────────────────────

🔐 *Premium AI Call System*
Voice cloning • Live bridge • SRTP encrypted
9 voices • 33 scripts • Auto pilot

────────────────────

👤 User: {escape_markdown_user(username)}
💰 Balance: {escape_markdown_user(days_left)}
📞 Calls: {rest_calls}
📦 Plan: {escape_markdown_user(plan)}'''
    if type(msg) == Message:
      await msg.answer_video(get_video())
      await msg.answer(message,reply_markup=keyboard, parse_mode='MarkdownV2')
      return
    await msg.answer()
    await msg.message.edit_text(message,reply_markup=keyboard, parse_mode='MarkdownV2')




async def start_refferals_command(message: Message, bot: Bot):
    user_id = message.from_user.id

    payload = message.text.split(maxsplit=1)[1].replace("/start ", "") if " " in message.text else ""

    new,users_count = is_new_user(user_id)
    if new:
        name = escape_markdown_user(message.from_user.first_name)
        if message.from_user.username:
            username = escape_markdown_user("@"+message.from_user.username)
        else:
            username = 'N/A'
        await bot.send_message(chat_id=get_admin()['id'],text=fr'''🆕 *New user*: {users_count}
*Username*\: {username}
*Name*\: `{name}`
*User ID*\: `{str(user_id)}`''',parse_mode='MarkdownV2')
        await add_user_fast(user_id)
    user_data = get_user_cached(user_id)
    if user_data['referred'] != True:
      try:
          referrer_id = int(payload[3:])
      except (ValueError, TypeError):
          referrer_id = None
      if user_id != referrer_id:
        if referrer_id != None:
            await update_user_cache(user_id, 'referred', True)
            referres = get_user_cached(referrer_id)
            referres = referres['referrals']+1
            await update_user_cache(referrer_id, 'referrals', referres)
    if user_data['banned']:
        return
    expiry_date = user_data['expiry_date']
    if message.from_user.username:
        username = f'@{message.from_user.username}'
    else:
        username = 'None'
    await start_proccess(message, username, expiry_date)


async def start_command(message: Message, bot: Bot):
    user_id = message.from_user.id
    new,users_count = is_new_user(user_id)
    if new:
        name = escape_markdown_user(message.from_user.first_name)
        if message.from_user.username:
            username = escape_markdown_user("@"+message.from_user.username)
        else:
            username = 'N/A'
        await bot.send_message(chat_id=get_groups()['new_users_ID'],text=fr'''🆕 *New user*: {users_count}
*Username*\: {username}
*Name*\: `{name}`
*User ID*\: `{str(user_id)}`''',parse_mode='MarkdownV2')
        await add_user_fast(user_id)
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    expiry_date = user_data['expiry_date']
    if message.from_user.username:
        username = f'@{message.from_user.username}'
    else:
        username = 'None'
    await start_proccess(message, username, expiry_date)

async def start_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    await state.clear()
    if user_data['banned']:
        return
    expiry_date = user_data['expiry_date']
    if callback.from_user.username:
        username = f'@{callback.from_user.username}'
    else:
        username = 'None'
    if callback.data.startswith('start_back:'):
        message_id = int(callback.data[11:])
        await bot.delete_message(user_id, message_id)
    await start_proccess(callback, username, expiry_date)










