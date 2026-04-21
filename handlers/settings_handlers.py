from config import get_scripts, get_script_audios
from utils import edit_text, generate_script ,remove_backslashes, is_valid_phone_number, check_subscription, get_user_cached, update_user_cache, escape_markdown_user, escape_markdown_text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram import Bot

def get_champ(script_name, user_id):
   user_data = get_user_cached(user_id)
   index = None
   i = 1 
   while index == None and i <= 5:
      
      script = user_data[f'cus_script{i}'].splitlines()[0]
      clean_script = remove_backslashes(script[3:len(script)-1])
      if clean_script == script_name:
         index = i
      i += 1
   return str(index)
      
def settings_message(expiry_date, caller_id, my_number, script, lang):
    if not(check_subscription(expiry_date)) or expiry_date=='N/A':
        plan = 'No subscription'
    else:
        plan = "Premium"
    if expiry_date != 'N/A':
      expiry_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
      days_left = str(expiry_date-datetime.now())
      days_left = days_left[:days_left.find(',')]
    else:
        days_left = '0 Days'
    if caller_id == 'Default':
        em = '🔀'
    elif caller_id == 'Random':
        em = '🎲'
    else:
        em = '📍'
    return fr'''⚙️ *Settings*
───────────────

👤 *Account*
• Days left: *{escape_markdown_user(days_left)}*
• Plan: *{plan}*
• Gateway: *ztn\_mx*

📞 *Call Settings*
• Caller ID: {em} *{caller_id}*
• My Number: `{my_number}`
• Script: *{escape_markdown_user(script)}*
• Language: *{lang}*

💡 _Tap to change settings_'''

def settings_keyboard(caller_id, my_number, script, lang):
    if caller_id == 'Default':
        em = '🔀'
    elif caller_id == 'Random':
        em = '🎲'
    else:
        em = '📍'
    return {
  "inline_keyboard": [
    [
      {
        "text": f"{em} Caller ID: {caller_id}",
        "callback_data": "callerid"
      }
    ],
    [
      {
        "text": f"📱 My Number: {my_number}",
        "callback_data": "mynumber"
      }
    ],
    [
      {
        "text": f"📜 Script: {script}",
        "callback_data": "script"
      }
    ],
    [
      {
        "text": f"🌍 Language: {lang}",
        "callback_data": "language"
      }
    ],
    [
      {
        "text": "📖 View ALL Scripts",
        "callback_data": "scripts"
      }
    ],
    [
      {
        "text": "⬅️ Back",
        "callback_data": "start_back"
      }
    ]
  ]
}

def build_script_keyboard(options, custom_scripts):
    rows = []
    for i in range(0, len(options), 2):
        pair = options[i:i+2]   # slice never raises, gives 1 or 2 items
        row = [{"text": opt, "callback_data": "script_" + opt} for opt in pair]
        rows.append(row)

    custom_scripts = custom_scripts[:5]
    if custom_scripts:
        rows.append([{"text": "—— Custom Script ——", "callback_data": "empty"}])
        for i in range(0, len(custom_scripts), 2):
            pair = custom_scripts[i:i+2]
            row = []
            for s in pair:
                first_line = s.splitlines()[0]
                if first_line.startswith("✅"):
                    display_text = "✅ ✏️ " + first_line[1:].lstrip()
                else:
                    display_text = "✏️ " + first_line
                row.append({"text": display_text, "callback_data": "script_custom_" + first_line})
            rows.append(row)

    rows.append([{"text": "➕ Create Custom Script", "callback_data": "custom_script"}])
    rows.append([{"text": "📁 Manage Custom Scripts", "callback_data": "manage_custom_scripts"}])
    rows.append([{"text": "⬅ Back", "callback_data": "settings_back"}])

    return {"inline_keyboard": rows}

def view_custom_scripts_keyboard(custom_scripts):
    rows = []
    
    for i in range(0, len(custom_scripts), 2):
        pair = custom_scripts[i:i+2]
        row = [{"text": "✏️ "+s.splitlines()[0], "callback_data": "view_custom_script_" + s.splitlines()[0]} for s in pair]
        rows.append(row)

    rows.append([{"text": "❌ Delete Scripts", "callback_data": "delete_scripts"}])
    rows.append([{"text": "⬅ Back", "callback_data": "scripts_list_back"}])
    
    return {"inline_keyboard": rows}

def delete_custom_scripts_keyboard(custom_scripts):
    rows = []
    
    for i in range(0, len(custom_scripts), 2):
        pair = custom_scripts[i:i+2]
        row = [{"text": "❌ "+s.splitlines()[0], "callback_data": "delete_script_" + s.splitlines()[0]} for s in pair]
        rows.append(row)
    
    rows.append([{"text": "⬅ Back", "callback_data": "manage_custom_scripts"}])
    
    return {"inline_keyboard": rows}

def script_keyboard(script, custom_scripts):
  options = [
    "Default",
    "Bank Security",
    "Delivery",
    "Amazon",
    "PayPal",
    "Crypto Exchange",
    "Insurance",
    "Telecom",
    "Email Security",
    "Tax Authority",
    "Marcus - Unauthorized Transfer",
    "Marcus - Login Alert",
    "Marcus - CD Withdrawal",
    "Marcus - Personal Loan",
    "Barclays - Fraud Alert",
    "Barclays - Login Alert",
    "Barclays - Wire Transfer",
    "Truist - Fraud Alert",
    "Truist - Account Access",
    "Truist - Zelle Transfer",
    "ID.me - Identity Verification",
    "ID.me - Suspicious Login",
    "ID.me - Benefits Verification",
    "Apple",
    "Google",
    "Microsoft",
    "Chase Bank",
    "Wells Fargo",
    "Bank of America",
    "Venmo",
    "Cash App",
    "Zelle",
    'ID.ME - Login Alert'
]
    
  if script in options:
    value = options.index(script)
    options[value] = '✅ '+script
  else:
    value = custom_scripts.index(script)
    custom_scripts[value] = '✅ '+script

  keyboard = build_script_keyboard(options, custom_scripts)
  return keyboard
  
def lang_keyboard(lang):
  options = [
    "🇺🇸 English",
    "🇪🇸 Spanish",
    "🇫🇷 French",
    "🇸🇦 Arabic",
    "🇧🇷 Portuguese ",
    "🇩🇪 German",
    "🇮🇹 Italian",
    "🇮🇳 Hindi",
    "🇨🇳 Chinese",
    "🇰🇷 Korean",
]
  value = options.index(lang)
  options[value] = '✅ '+lang
  return {"inline_keyboard": [
    [
      {
        "text": options[0],
        "callback_data": "lang_"+options[0]
      },
      {"text": options[1],
        "callback_data": "lang_"+options[1]
      }
    ],
    [
      {
        "text": options[2],
        "callback_data": "lang_"+options[2]
      },
      {"text": options[3],
        "callback_data": "lang_"+options[3]
      }
    ],[
      {
        "text": options[4],
        "callback_data": "lang_"+options[4]
      },
      {"text": options[5],
        "callback_data": "lang_"+options[5]
      }
    ],[
      {
        "text": options[6],
        "callback_data": "lang_"+options[6]
      },
      {"text": options[7],
        "callback_data": "lang_"+options[7]
      }
    ],[
      {
        "text": options[8],
        "callback_data": "lang_"+options[8]
      },
      {"text": options[9],
        "callback_data": "lang_"+options[9]
      }
    ],[
      {
        "text": "⬅ Back",
        "callback_data": "settings_back"
      }
    ]
  ]
}

def view_script_keyboard():
  options = [
    "Default",
    "Bank Security",
    "Delivery",
    "Amazon",
    "PayPal",
    "Crypto Exchange",
    "Insurance",
    "Telecom",
    "Email Security",
    "Tax Authority",
    "Marcus - Unauthorized Transfer",
    "Marcus - Login Alert",
    "Marcus - CD Withdrawal",
    "Marcus - Personal Loan",
    "Barclays - Fraud Alert",
    "Barclays - Login Alert",
    "Barclays - Wire Transfer",
    "Truist - Fraud Alert",
    "Truist - Account Access",
    "Truist - Zelle Transfer",
    "ID.me - Identity Verification",
    "ID.me - Suspicious Login",
    "ID.me - Benefits Verification",
    "Apple",
    "Google",
    "Microsoft",
    "Chase Bank",
    "Wells Fargo",
    "Bank of America",
    "Venmo",
    "Cash App",
    "Zelle",
    'ID.ME - Login Alert'
]
  return {"inline_keyboard": [
    [
      {
        "text": options[0],
        "callback_data": "view_script_"+options[0]
      },
      {"text": options[1],
        "callback_data": "view_script_"+options[1]
      }
    ],
    [
      {
        "text": options[2],
        "callback_data": "view_script_"+options[2]
      },
      {"text": options[3],
        "callback_data": "view_script_"+options[3]
      }
    ],[
      {
        "text": options[4],
        "callback_data": "view_script_"+options[4]
      },
      {"text": options[5],
        "callback_data": "view_script_"+options[5]
      }
    ],[
      {
        "text": options[6],
        "callback_data": "view_script_"+options[6]
      },
      {"text": options[7],
        "callback_data": "view_script_"+options[7]
      }
    ],[
      {
        "text": options[8],
        "callback_data": "view_script_"+options[8]
      },
      {"text": options[9],
        "callback_data": "view_script_"+options[9]
      }
    ],[
      {
        "text": options[10],
        "callback_data": "view_script_"+options[10]
      },
      {"text": options[11],
        "callback_data": "view_script_"+options[11]
      }
    ],[
      {
        "text": options[12],
        "callback_data": "view_script_"+options[12]
      },
      {"text": options[13],
        "callback_data": "view_script_"+options[13]
      }
    ],[
      {
        "text": options[14],
        "callback_data": "view_script_"+options[14]
      },
      {"text": options[15],
        "callback_data": "view_script_"+options[15]
      }
    ],[
      {
        "text": options[16],
        "callback_data": "view_script_"+options[16]
      },
      {"text": options[17],
        "callback_data": "view_script_"+options[17]
      }
    ],[
      {
        "text": options[18],
        "callback_data": "view_script_"+options[18]
      },
      {"text": options[19],
        "callback_data": "view_script_"+options[19]
      }
    ],[
      {
        "text": options[20],
        "callback_data": "view_script_"+options[20]
      },
      {"text": options[21],
        "callback_data": "view_script_"+options[21]
      }
    ],[
      {
        "text": options[22],
        "callback_data": "view_script_"+options[22]
      },
      {"text": options[23],
        "callback_data": "view_script_"+options[23]
      }
    ],[
      {
        "text": options[24],
        "callback_data": "view_script_"+options[24]
      },
      {"text": options[25],
        "callback_data": "view_script_"+options[25]
      }
    ],[
      {
        "text": options[26],
        "callback_data": "view_script_"+options[26]
      },
      {"text": options[27],
        "callback_data": "view_script_"+options[27]
      }
    ],[
      {
        "text": options[28],
        "callback_data": "view_script_"+options[28]
      },
      {"text": options[29],
        "callback_data": "view_script_"+options[29]
      }
    ],[
      {
        "text": options[30],
        "callback_data": "view_script_"+options[30]
      },
      {"text": options[31],
        "callback_data": "view_script_"+options[31]
      }
    ],[
      {
        "text": options[32],
        "callback_data": "view_script_"+options[32]
      }
    ],[
      {
        "text": "⬅ Back",
        "callback_data": "settings_back"
      }
    ]
  ]
}

async def settings_proccess(callback, expiry_date, caller_id, my_number, script, lang):
    keyboard = settings_keyboard(caller_id, my_number, script, lang)
    message = settings_message(expiry_date, caller_id, my_number, script, lang)
    await callback.answer()
    await callback.message.edit_text(message,reply_markup=keyboard, parse_mode='MarkdownV2')

async def caller_id_proccess(callback, expiry_date, caller_id, my_number, script, lang, user_id):
  if  caller_id == "Default":
      await update_user_cache(user_id, 'caller_id', 'Random')
      caller_id = 'Random'
  elif caller_id == "Random":
      await update_user_cache(user_id, 'caller_id', 'Fixed')
      caller_id = 'Fixed'
  else:
      await update_user_cache(user_id, 'caller_id', 'Default')
      caller_id = 'Default'

  keyboard = settings_keyboard(caller_id, my_number, script, lang)
  
  message = settings_message(expiry_date, caller_id, my_number, script, lang)
  await callback.answer()
  await callback.message.edit_text(message,reply_markup=keyboard, parse_mode='MarkdownV2')

async def script_proccess(callback, script, user_id):
  if script.find('*') != -1:
    script = script[3:len(script)-1]

  scripts = []
  user_data = get_user_cached(user_id)
  for i in range(1,6):
    if user_data['cus_script'+str(i)] != 'N/A':
        clean_script = user_data['cus_script'+str(i)].splitlines()[0]
        clean_script = clean_script[3:len(clean_script)-1]
        scripts.append(remove_backslashes(clean_script))
  keyboard = script_keyboard(script, scripts)
  await callback.answer()
  await callback.message.edit_text(fr'''📜 *Select Call Script*

Current: *{escape_markdown_user(script)}*

Tap a script to use it\.
Or create your own custom script\!''',reply_markup=keyboard, parse_mode='MarkdownV2')

async def change_script_proccess(callback, script, user_id):
  if callback.data == 'settings_back':
      user_data = get_user_cached(user_id)
      expiry_date,caller_id, my_number, script, lang = user_data['expiry_date'],user_data['caller_id'],user_data['my_number'],user_data['script'],user_data['lang']
      await settings_proccess(callback, expiry_date, caller_id, my_number, script, lang)
      return
  if callback.data.startswith("script_custom_"):
      script = callback.data[14:]
  else:
    script = callback.data[7:]
  scripts = []
  user_data = get_user_cached(user_id)
  for i in range(1,6):
    if user_data['cus_script'+str(i)] != 'N/A':
        clean_script = user_data['cus_script'+str(i)].splitlines()[0]
        clean_script = clean_script[3:len(clean_script)-1]
        scripts.append(remove_backslashes(clean_script))



  keyboard = script_keyboard(script, scripts)
  
  await callback.answer('Script set: '+script, show_alert=True)
  await callback.message.edit_text(fr'''📜 *Select Call Script*

Current: *{escape_markdown_user(script)}*

Tap a script to use it\.
Or create your own custom script\!''',reply_markup=keyboard, parse_mode='MarkdownV2')
  await update_user_cache(user_id, 'script', script)

async def lang_proccess(callback, lang):

  keyboard = lang_keyboard(lang)
  
  await callback.answer()
  await callback.message.edit_text(fr'''🌍 Select Language

Choose the language for call scripts\.
The TTS voice will match the selected language\.

Current: {lang}''',reply_markup=keyboard, parse_mode='MarkdownV2')

async def change_lang_proccess(callback, user_id):
  if callback.data == 'settings_back':
      user_data = get_user_cached(user_id)
      expiry_date,caller_id, my_number, script, lang = user_data['expiry_date'],user_data['caller_id'],user_data['my_number'],user_data['script'],user_data['lang']
      await settings_proccess(callback, expiry_date, caller_id, my_number, script, lang)
      return
  lang = callback.data[5:]

  keyboard = lang_keyboard(lang)
  
  await callback.answer()
  await callback.message.edit_text(fr'''🌍 Select Language

Choose the language for call scripts\.
The TTS voice will match the selected language\.

Current: {lang}''',reply_markup=keyboard, parse_mode='MarkdownV2')
  await update_user_cache(user_id, 'lang', lang)

async def view_one_script_proccess(callback):
  script = callback.data[12:]

  options = [
    "Default",
    "Bank Security",
    "Delivery",
    "Amazon",
    "PayPal",
    "Crypto Exchange",
    "Insurance",
    "Telecom",
    "Email Security",
    "Tax Authority",
    "Marcus - Unauthorized Transfer",
    "Marcus - Login Alert",
    "Marcus - CD Withdrawal",
    "Marcus - Personal Loan",
    "Barclays - Fraud Alert",
    "Barclays - Login Alert",
    "Barclays - Wire Transfer",
    "Truist - Fraud Alert",
    "Truist - Account Access",
    "Truist - Zelle Transfer",
    "ID.me - Identity Verification",
    "ID.me - Suspicious Login",
    "ID.me - Benefits Verification",
    "Apple",
    "Google",
    "Microsoft",
    "Chase Bank",
    "Wells Fargo",
    "Bank of America",
    "Venmo",
    "Cash App",
    "Zelle",
    "ID.ME - Login Alert"
]
  index = options.index(script)
  keyboard = {"inline_keyboard": [
    [
      {
        "text": "✅ Use This Script",
        "callback_data": "set_script_"+script
      }
    ],
    [
      {
        "text": "🔊 Lisen Greeting",
        "callback_data": "greeting_"+script
      },
      {
        "text": "🔊 Lisen Goodbye",
        "callback_data": "goodbye_"+script
      }
    ],
    [
      {
        "text": '⬅ Back',
        "callback_data": "scripts_back"
      }
    ]]}
  message = escape_markdown_text(get_scripts()[index])
  await callback.answer()
  await callback.message.edit_text(message,reply_markup=keyboard, parse_mode='MarkdownV2')
  
async def view_script_proccess(callback):

  keyboard = view_script_keyboard()
  
  await callback.answer()
  await callback.message.edit_text(fr'''📖 *View Script Content*

Tap a script to see what it says:''',reply_markup=keyboard, parse_mode='MarkdownV2')

async def set_script_proccess(callback, user_id):
  if callback.data == 'scripts_back':
      await view_script_proccess(callback)
      return
  script = callback.data[11:]
  user_data = get_user_cached(user_id)
  expiry_date,caller_id, my_number, lang = user_data['expiry_date'],user_data['caller_id'],user_data['my_number'],user_data['lang']
  await callback.answer(fr'Script set: {script}', show_alert=True)
  await settings_proccess(callback, expiry_date,caller_id, my_number, script, lang)
  await update_user_cache(user_id, 'script', script)

async def create_script_proccess(callback, user_id):
  user_data = get_user_cached(user_id)
  if user_data['cus_script1'] != 'N/A' and user_data['cus_script2'] != 'N/A' and user_data['cus_script3'] != 'N/A' and user_data['cus_script4'] != 'N/A' and user_data['cus_script5'] != 'N/A':
      keyboard = {"inline_keyboard": [
    [
      {
        "text": "📁 Manage Custom Scripts",
        "callback_data": "manage_custom_scripts"
      }
    ],
    [
      {
        "text": '⬅ Back',
        "callback_data": "scripts_list_back"
      }
    ]]}
      await callback.message.edit_text(r'''❌ *Limit Reached*

You can have up to 5 custom scripts\.
Delete one first to create a new one\.''',reply_markup=keyboard, parse_mode='MarkdownV2')
      return
  keyboard = {"inline_keyboard": [
    [
    {
      "text": "🤖 AI Generate",
      "callback_data": "AI_generate_script"
    }
    ],
    [
      {
        "text": "✏️ Manual",
        "callback_data": "manual_generate_script"
      }
    ],
    [
      {
        "text": '⬅ Back',
        "callback_data": "scripts_list_back"
      }
    ]]}
  await callback.message.edit_text(r"""✏️ *Create Custom Script*
───────────────

Choose how to create your script:""",reply_markup=keyboard, parse_mode='MarkdownV2')

async def script_name_proccess(callback, state):
    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel", "callback_data": "scripts_list_back"}]
        ]
    }

    await callback.message.edit_text(r"""✏️ *Create Custom Script*
───────────────

*Step 1/4: Script Name*

Send a name for your script\.
Example: `My Bank Script`

*Variables you can use*:
`{name}` \- Contact name
`{service}` \- Service name
`{digits}` \- OTP digit count
`{amount}` \- Amount
`{code}` \- Received code \(confirm only\)""",
        reply_markup=keyboard, parse_mode='MarkdownV2' 
    )

    await state.set_state(ScriptForm.waiting_for_name)

async def manage_scripts_proccess(callback, user_id):
  user_data = get_user_cached(user_id)
  if user_data['cus_script1'] == 'N/A' and user_data['cus_script2'] == 'N/A' and user_data['cus_script3'] == 'N/A' and user_data['cus_script4'] == 'N/A' and user_data['cus_script5'] == 'N/A':
      keyboard = {"inline_keyboard": [
    [
      {
        "text": '⬅ Back',
        "callback_data": "scripts_list_back"
      }
    ]]}
      await callback.message.edit_text('''❌ You don't have any custom script''',reply_markup=keyboard)
      return
  scripts = []
  user_data = get_user_cached(user_id)
  for i in range(1,6):
    if user_data['cus_script'+str(i)] != 'N/A':
        clean_script = user_data['cus_script'+str(i)].splitlines()[0]
        clean_script = clean_script[3:len(clean_script)-1]
        scripts.append(remove_backslashes(clean_script))
  keyboard =  view_custom_scripts_keyboard(scripts)
  await callback.message.edit_text(r"""📁 *Manage Custom Scripts*:

Tap on the script you want to view bellow\.""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def view_one_custom_script_proccess(callback, user_id):
  script = callback.data[19:]
  scripts = []
  user_data = get_user_cached(user_id)
  for i in range(1,6):
    if user_data['cus_script'+str(i)] != 'N/A':
        clean_script = user_data['cus_script'+str(i)].splitlines()[0]
        clean_script = clean_script[3:len(clean_script)-1]
        scripts.append(remove_backslashes(clean_script))

  index = scripts.index(script)
  script1 = user_data['cus_script'+str(index+1)]
  keyboard = {"inline_keyboard": [
    [
      {
        "text": "✅ Use This Script",
        "callback_data": "set_script_"+script
      }
    ],
    [
      {
        "text": '⬅ Back',
        "callback_data": "manage_custom_scripts"
      }
    ]]}
  await callback.answer()
  await callback.message.edit_text(script1,reply_markup=keyboard, parse_mode='MarkdownV2')

async def delete_scripts_proccess(callback, user_id):
  user_data = get_user_cached(user_id)
  scripts = []
  user_data = get_user_cached(user_id)
  if user_data['cus_script1'] == 'N/A' and user_data['cus_script2'] == 'N/A' and user_data['cus_script3'] == 'N/A' and user_data['cus_script4'] == 'N/A' and user_data['cus_script5'] == 'N/A':
      keyboard = {"inline_keyboard": [
    [
      {
        "text": '⬅ Back',
        "callback_data": "scripts_list_back"
      }
    ]]}
      await callback.message.edit_text('''❌ You don't have any custom script''',reply_markup=keyboard)
      return
  for i in range(1,6):
    if user_data['cus_script'+str(i)] != 'N/A':
        clean_script = user_data['cus_script'+str(i)].splitlines()[0]
        clean_script = clean_script[3:len(clean_script)-1]
        scripts.append(remove_backslashes(clean_script))
  keyboard =  delete_custom_scripts_keyboard(scripts)
  await callback.message.edit_text(r"""❌ *Delete Custom Scripts*:

Tap on the script bellow to delete\.""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def confirm_delete_scripts_proccess(callback, script):
  keyboard =  {
  "inline_keyboard": [
    [
      {
        "text": f"✅ Confirm",
        "callback_data": f"confirm_delete_{script}"
      }
    ],
    [
      {
        "text": f"⬅ Back",
        "callback_data": "delete_scripts"
      }
    ]
  ]
}
  await callback.message.edit_text(fr"""❌ *Delete {script}*:

Tap on _comfirm_ bellow to confirm deleting the script\.""", reply_markup=keyboard, parse_mode='MarkdownV2')

async def delete_script_proccess(callback, script, user_id):
  user_data = get_user_cached(user_id)
  keyboard =  {
  "inline_keyboard": [
    [
      {
        "text": f"⬅ Back",
        "callback_data": "delete_scripts"
      }
    ]
  ]
}
  index = get_champ(script, user_id)

  if user_data['script'] == script:
     await update_user_cache(user_id, 'script', 'Default')

  await callback.message.edit_text(f"""✅ {escape_markdown_user(script)} deleted successfully.""", reply_markup=keyboard)
  await update_user_cache(user_id, 'cus_script'+index, 'N/A')

async def get_discription_proccess(callback, state):
    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel", "callback_data": "scripts_list_back"}]
        ]
    }

    await callback.message.edit_text(r"""🤖 *AI Script Generator*
───────────────

Describe the script you want and AI will generate it\.

*Examples*:
• _Bank fraud alert about suspicious wire transfer_
• _Amazon purchase verification for expensive item_
• _Apple ID security alert, someone trying to reset password_
• _IRS tax refund verification call_
• _Credit card company calling about unusual charges_

Send your description:""",
        reply_markup=keyboard, parse_mode='MarkdownV2' 
    )

    await state.set_state(ScriptForm.waiting_for_discription)

async def lisen_script_proccess(bot, callback, user_id):
  message = callback.data
  if message.startswith('greeting_'):
    script = callback.data[9:]
    type = 'greeting'
  else:
     script = callback.data[8:]
     type = 'goodbye'

  audio = get_script_audios().get(script, {})
  audio_file_id = audio.get(type)
  if not audio_file_id:
        await callback.answer("⚠️ No audio set for this script yet.", show_alert=True)
        return
  caption = f'🔊 {script} - {type.capitalize()}'
  await callback.answer('🔊 Generating audio...')
  await bot.send_voice(user_id,audio_file_id ,caption=caption)
  

# --- STATE DEFINITION ---
class ScriptForm(StatesGroup):
    waiting_for_number = State()
    waiting_for_discription = State()
    waiting_for_name = State()
    waiting_for_greeting = State()
    waiting_for_code = State()
    waiting_for_goodbye = State()

async def process_my_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    number = message.text.strip()
    if number[0] != "+":
        number = "+"+number
    if not is_valid_phone_number(number):
        await message.answer("❌ Invalid number format.")
        return
    await update_user_cache(user_id, 'my_number',number)

    await message.answer(f"✅ Your number set to: {number}")
    await state.clear()  # reset FSM state

async def settings_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    
    await state.clear()
    expiry_date,caller_id, my_number, script, lang = user_data['expiry_date'],user_data['caller_id'],user_data['my_number'],remove_backslashes(user_data['script']),user_data['lang']
    await settings_proccess(callback, expiry_date, caller_id, my_number, script, lang)

async def caller_id_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    expiry_date,caller_id, my_number, script, lang = user_data['expiry_date'],user_data['caller_id'],user_data['my_number'],user_data['script'],user_data['lang']
    await caller_id_proccess(callback, expiry_date, caller_id, my_number, script, lang, user_id)

async def my_number_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)

    if user_data['banned']:
        return
    keyboard = {"inline_keyboard": [
      [
        {
          "text": "⬅️ Back",
          "callback_data": "settings"
        }
      ]
    ]}
    await callback.message.edit_text("""📱 Send your phone number in E.164 format:
Example: +12125551234""", reply_markup=keyboard)
    await state.set_state(ScriptForm.waiting_for_number)

async def script_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await state.clear()
    script = remove_backslashes(user_data['script'])
    await script_proccess(callback, script, user_id)

async def change_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    script = remove_backslashes(user_data['script'])
    await change_script_proccess(callback, script, user_id)

async def language_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    lang = user_data['lang']
    await lang_proccess(callback, lang)

async def change_lang_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await change_lang_proccess(callback, user_id)

async def view_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await view_script_proccess(callback)

async def view_one_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await view_one_script_proccess(callback)

async def set_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await set_script_proccess(callback, user_id)

async def create_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await create_script_proccess(callback, user_id)

async def script_name_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)

    if user_data['banned']:
        return

    await script_name_proccess(callback, state)

async def script_name_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)

    if user_data['banned']:
        return

    await state.update_data(name=message.text)
    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel", "callback_data": "scripts_list_back"}]
        ]
    }
    await message.answer(r"""✏️ *Step 2/4: Greeting*

Send the greeting message\.
This is played when the call is answered\.

Example:
`Hello {name}\. This is {service} security\. We detected suspicious activity on your account\. Press 1 to verify your identity\.`""",reply_markup=keyboard, parse_mode='MarkdownV2' )
    await state.set_state(ScriptForm.waiting_for_greeting)

async def script_greeting_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)

    if user_data['banned']:
        return

    await state.update_data(greeting=message.text)
    keyboard = {
        "inline_keyboard": [
            [{"text": "❌ Cancel", "callback_data": "scripts_list_back"}]
        ]
    }
    await message.answer(r"""✏️ *Step 3/4: Code Request*

Send the message asking for the OTP code\.

Example:
`Please enter your {digits}-digit verification code followed by the pound key\.`""",reply_markup=keyboard, parse_mode='MarkdownV2' )
    await state.set_state(ScriptForm.waiting_for_code)

async def script_code_handler(message: Message, state: FSMContext):
  user_id = message.from_user.id
  user_data = get_user_cached(user_id)

  if user_data['banned']:
      return

  await state.update_data(code=message.text)
  keyboard = {
      "inline_keyboard": [
          [{"text": "❌ Cancel", "callback_data": "scripts_list_back"}]
      ]
  }
  await message.answer(r"""✏️ *Step 4/4: Goodbye*

Send the goodbye message after code is accepted\.

Example:
`Your identity has been verified\. Your account is now secure\. Thank you\. Goodbye\.`""", reply_markup=keyboard, parse_mode='MarkdownV2' )
  await state.set_state(ScriptForm.waiting_for_goodbye)

async def script_goodbye_handler(message: Message, state: FSMContext):
  user_id = message.from_user.id
  user_data = get_user_cached(user_id)

  if user_data['banned']:
      return

  await state.update_data(goodbye=message.text)

  data = await state.get_data()

  name = data.get("name")
  greeting = data.get("greeting")
  code = data.get("code")
  goodbye = data.get("goodbye")

  full_script = fr"""📜 *{escape_markdown_user(name)}*

*Greeting:*
{escape_markdown_user(greeting)}

*Code Request*:
{escape_markdown_user(code)}

*Goodbye*:
{escape_markdown_user(goodbye)}"""
  keyboard = {
      "inline_keyboard": [
          [{"text": "⚙️ Settings", "callback_data": "settings"}]
      ]
  }
  await message.answer(fr"""✅ *Custom Script Created\!*

{full_script}

This script is now your default\.""", reply_markup=keyboard, parse_mode='MarkdownV2' )

  await state.clear()
  if user_data['cus_script1'] == 'N/A':
      await update_user_cache(user_id, 'cus_script1', full_script)
  elif user_data['cus_script2'] == 'N/A':
      await update_user_cache(user_id, 'cus_script2', full_script)
  elif user_data['cus_script3'] == 'N/A':
      await update_user_cache(user_id, 'cus_script3', full_script)
  elif user_data['cus_script4'] == 'N/A':
      await update_user_cache(user_id, 'cus_script4', full_script)
  elif user_data['cus_script5'] == 'N/A':
      await update_user_cache(user_id, 'cus_script5', full_script)
  await update_user_cache(user_id, 'script', name)

async def manage_scripts_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await manage_scripts_proccess(callback, user_id)

async def view_one_custom_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await view_one_custom_script_proccess(callback, user_id)

async def delete_scripts_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await delete_scripts_proccess(callback, user_id)

async def confirm_delete_scripts_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    script = callback.data[14:]
    await confirm_delete_scripts_proccess(callback, script)

async def delete_script_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    script = callback.data[15:]
    await delete_script_proccess(callback, script, user_id)

async def get_discription_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)

    if user_data['banned']:
        return

    await get_discription_proccess(callback, state)

async def process_my_AI_script(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_cached(user_id)
    description = message.text.strip()
    loading_msg = await message.answer('🤖 Generating script with AI...')
    script = await generate_script(description)
    title, full_script = edit_text(script)
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔄 Regenerate", "callback_data": "AI_generate_script"}],
            [{"text": "⚙️ Settings", "callback_data": "settings_back"}]
        ]
    }
    await loading_msg.edit_text(fr"""✅ *AI Script Created*\!
───────────────

{escape_markdown_text(full_script)}

This script is now your default\.""", reply_markup=keyboard ,parse_mode='MarkdownV2')
    await update_user_cache(user_id, 'script', title)
    full_script = escape_markdown_text(full_script)
    if user_data['cus_script1'] == 'N/A':
      await update_user_cache(user_id, 'cus_script1', full_script)
    elif user_data['cus_script2'] == 'N/A':
        await update_user_cache(user_id, 'cus_script2', full_script)
    elif user_data['cus_script3'] == 'N/A':
        await update_user_cache(user_id, 'cus_script3', full_script)
    elif user_data['cus_script4'] == 'N/A':
        await update_user_cache(user_id, 'cus_script4', full_script)
    elif user_data['cus_script5'] == 'N/A':
        await update_user_cache(user_id, 'cus_script5', full_script)
    await state.clear()

async def lisen_script_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await lisen_script_proccess(bot, callback, user_id)
