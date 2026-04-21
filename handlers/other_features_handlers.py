from config import get_admin
from utils import ask_grok, escape_markdown_Ai_text, get_user_cached
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


async def history_proccess(msg):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": "start_back"
      }
    ]
  ]
}


    await msg.message.edit_text('No call history.',reply_markup=keyboard)

async def leaderboard_proccess(msg):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "🔄 Refresh",
        "callback_data": "refresh_leaderboard"
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


    await msg.message.edit_text(r'''🏆 *Weekly Leaderboard*
───────────────

📞 *Most Calls*
🥇 8172741222 — *2987* calls
🥈 8525768766 — *1565* calls
🥉 8313193451 — *1464* calls
4️⃣ 8367908315 — *1464* calls
5️⃣ 7453489529 — *1443* calls

🎯 *Most Successful*
🥇 7453489529 — *352* successful
🥈 7658967089 — *334* successful
🥉 7275541943 — *332* successful
4️⃣ 8313193451 — *319* successful
5️⃣ 7112788423 — *305* successful

───────────────
👤 *Your Stats \(7 days\)*
• Calls: 0
• Successful: 0
• Duration: 0m 0s''',reply_markup=keyboard, parse_mode='MarkdownV2')

async def refresh_proccess(msg):
    await msg.answer()

async def earn_proccess(msg,user_id, referrals):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": "start_back"
      }
    ]
  ]
}


    await msg.message.edit_text(fr'''🎁 *Referral Program*

Share your link 15 times and earn:
• 15 PayPal Logs
• 10% bonus on their first purchase

Your link:
`https://t\.me/debugDRAGON\_bot?start\=ref{user_id}`

Total referrals: *{referrals}*''',reply_markup=keyboard, parse_mode='MarkdownV2')

async def ask_ai_proccess(callback, state):
    await callback.answer()
    await state.set_state(AIChat.chatting)
    await state.update_data(history=[])
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "💬 Contact Admin",
        "url": get_admin()['link']
      }
    ],
    [
      {
        "text": "❌ End Chat",
        "callback_data": "start_back"
      }
    ]
  ]
}
    await callback.message.edit_text(
        r"""🤖 *AI Assistant*
───────────────

Hey\! I'm your AI assistant\.
Ask me anything about the bot and I'll help you\.

💬 *Just type your question*\.\.\.

💡 Try:
• _How do I make a call?_
• _What are the prices?_
• _How to change language?_""",reply_markup=keyboard, parse_mode='MarkdownV2'
    )



class AIChat(StatesGroup):
    chatting = State()


async def history_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await history_proccess(callback)

async def leaderboard_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await leaderboard_proccess(callback)

async def refresh_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await refresh_proccess(callback)

async def earn_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    referrals = user_data['referrals']
    await earn_proccess(callback, user_id, referrals)

async def ask_ai_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await ask_ai_proccess(callback, state)

async def ai_chat_message(message: Message, state: FSMContext): 
    data = await state.get_data()
    history = data.get("history", [])
 
    history.append({"role": "user", "content": str(message.text)})
 
    thinking = await message.answer("🤖 Thinking...")
 
    try:
        answer = await ask_grok(history)
        history.append({"role": "assistant", "content": answer})
 
        # keep last 10 messages to avoid token overflow
        if len(history) > 10:
            history = history[-10:]
        keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "❌ End Chat",
        "callback_data": "start_back"
      }
    ]
  ]
}
        await state.update_data(history=history)
        await thinking.edit_text(f"🤖 {escape_markdown_Ai_text(answer)}", reply_markup=keyboard, parse_mode='MarkdownV2')
 
    except Exception as e:
        print(str(e))
        await thinking.edit_text("❌ Something went wrong, please try again.")
