from utils import escape_markdown_user, get_user_cached, get_email_info ,escape_markdown_Ai_text, get_phone_info, get_ip_info
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


async def tools_proccess(msg):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "📧 Email Lookup",
        "callback_data": "email_lookup"
      },
      {
        "text": "📞 Number Info",
        "callback_data": "number_info"
      }
    ],
    [
      {
        "text": "🌐 IP Lookup",
        "callback_data": "ip_lookup"
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


    await msg.message.edit_text('''🧰 Tools
───────────────''',reply_markup=keyboard)

async def email_lookup_proccess(msg, state):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": "tools"
      }
    ]
  ]
}


    await msg.message.edit_text(r'''*Email Lookup*

Send me an email address to analyze\.

I will check:
\- Format validation
\- Domain info and MX records
\- Disposable email detection
\- Domain reputation''',reply_markup=keyboard, parse_mode='MarkdownV2')
    await state.set_state(Tools.email_lookup)

async def number_lookup_proccess(msg, state):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": "tools"
      }
    ]
  ]
}


    await msg.message.edit_text(r'''*Number Info Lookup*

Send me a phone number with country code\.
Example: `\+12025551234`

I will check:
\- Carrier name
\- Location / Country
\- Line type \(Mobile/Landline/VOIP\)
\- Timezone''',reply_markup=keyboard, parse_mode='MarkdownV2')
    await state.set_state(Tools.number_lookup)

async def ip_lookup_proccess(msg, state):
    keyboard = {
  "inline_keyboard": [
    [
      {
        "text": "⬅ Back",
        "callback_data": "tools"
      }
    ]
  ]
}


    await msg.message.edit_text(r'''🌐 *IP Lookup*
───────────────

Send an IP address to lookup:

Example: `8\.8\.8\.8`''',reply_markup=keyboard, parse_mode='MarkdownV2')
    await state.set_state(Tools.ip_lookup)


class Tools(StatesGroup):
    email_lookup = State()
    number_lookup = State()
    ip_lookup = State()



async def tools_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await state.clear()
    await tools_proccess(callback)

async def email_lookup_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await email_lookup_proccess(callback, state)

async def email_checking_message(message: Message, state: FSMContext): 
    email = message.text
    info = get_email_info(email)
    try:
        email = info['email']
        local = info['local']
        domain = info['domain']
        format_valid =  info['format_valid']
        if format_valid:
            format = r'✅ *Format*: valid'
        else:
            format = r'❌ *Format*: invalid'
        mx_found =  info['mx_found']
        if mx_found :
            mx = r'✅ *MX Records*: Found'
        else:
            mx = r'❌ *MX Records*: Not Found'
        a_found =  info['a_found']
        if a_found :
            a = r'*DNS \(A Record\)*: Found'
        else:
            a = r'*DNS \(A Record\)*: Not Found'
        provider =  info['provider']
        disposable =  info['disposable']
        if not disposable :
            dis = r'✅ *Disposable*: No'
        else:
            dis = r'❌ *Disposable*: Yes'
        
        mx_records =  info['mx_records']
        records = ''
        for i in range(len(mx_records)):
            records = records+f' {i+1}. `{mx_records[i]}`\n'
        ip_addresses =  info['ip_addresses']
        ips = ''
        for i in range(len(ip_addresses)):
            ips = ips+f' - `{ip_addresses[i]}`\n'
        score =  info['score']
        score_bar =  info['score_bar']
        msg = fr"""*Email Lookup Results*
\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=

*Email*: `{escape_markdown_user(email)}`
*Local Part*: `{escape_markdown_user(local)}`
*Domain*: `{escape_markdown_user(domain)}`

\-\- *Validation* \-\-
{format}
{mx}
{a}

\-\- *Provider Info* \-\-
*Provider*: {escape_markdown_user(provider)}
{dis}

\-\- *MX Records* \-\-
{escape_markdown_Ai_text(records)}

\-\- *IP Addresses* \-\-
{escape_markdown_Ai_text(ips)}

*Deliverability Score*: {score}/100
`{escape_markdown_user(score_bar)}`"""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🔄 Lookup Another",
            "callback_data": "email_lookup"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "tools"
        }
        ]
    ]
    }
        await message.answer(msg, parse_mode="MarkdownV2", reply_markup=keyboard)
    except:
        msg = fr"""❌ *Invalid email format\!*

`{escape_markdown_user(email)}` is not a valid email address\.

Please send a valid email address\."""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🔄 Try Again",
            "callback_data": "email_lookup"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "tools"
        }
        ]
    ]
    }
        await message.answer(msg, parse_mode="MarkdownV2", reply_markup=keyboard)




    await state.clear()

async def number_lookup_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await number_lookup_proccess(callback, state)

async def number_checking_message(message: Message, state: FSMContext): 
    number = message.text
    info = get_phone_info(number)
    try:
        number = info['number']
        e164 = info['e164']
        national = info['national']
        country_code =  info['country_code']
        national_number =  info['national_number']
        valid =  info['valid']
        if valid:
            valid = '✅ *Valid*: Yes'
        else:
            valid = '❌ *Valid*: No'
        possible =  info['possible']
        if possible:
            possible = 'Yes'
        else:
            possible = 'No'
        type =  info['type']
        carrier =  info['carrier']
        if carrier == '':
            carrier = 'Unknown'
        location =  info['location']
        region =  info['region']
        timezones =  info['timezones']
        msg = fr"""*Phone Number Info*
\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=

*Number*: `{escape_markdown_user(number)}`
*E\.164*: `{escape_markdown_user(e164)}`
*National*: `{escape_markdown_user(national)}`
*Country Code*: {escape_markdown_user(country_code)}
*National Number*: `{escape_markdown_user(national_number)}`

\-\- *Validation* \-\-
{valid}
  *Possible*: {possible}

\-\- *Details* \-\-
📲 *Type*: {escape_markdown_user(type)}
*Carrier*: {escape_markdown_user(carrier)}
*Location*: {escape_markdown_user(location)}
*Region*: {region}

\-\- *Timezone* \-\-
  \- `{escape_markdown_user(timezones[0])}`"""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🔄 Lookup Another",
            "callback_data": "number_info"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "tools"
        }
        ]
    ]
    }
        await message.answer(msg, parse_mode="MarkdownV2", reply_markup=keyboard)
    except:
        if number[0] != '+':
            number = '+'+number
        msg = fr"""❌ *Invalid phone number\!*

`{escape_markdown_user(number)}` could not be parsed\.

Make sure to include the country code\.
Example: `\+12025551234`"""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🔄 Try Again",
            "callback_data": "number_info"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "tools"
        }
        ]
    ]
    }
        await message.answer(msg, parse_mode="MarkdownV2", reply_markup=keyboard)




    await state.clear()

async def ip_lookup_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = get_user_cached(user_id)
    if user_data['banned']:
        return
    await ip_lookup_proccess(callback, state)

async def ip_checking_message(message: Message, state: FSMContext): 
    ip = message.text
    info = await get_ip_info(ip)
    try:
        ip = info['ip']
        country = info['country']
        region = info['region']
        city =  info['city']
        zip =  info['zip']
        timezone =  info['timezone']
        coords =  info['coords']
        isp =  info['isp']
        org =  info['org']
        asn=  info['asn']
        proxy_vpn =  info['proxy_vpn']
        if proxy_vpn:
            proxy_vpn = "❌ Yes"
        else:
            proxy_vpn = "✅ No"
        hosting =  info['hosting']
        if hosting:
            hosting = '⚠️ Yes'
        else:
            hosting = '✅ No'
        msg = fr"""🌐 *IP Lookup Results*
───────────────

📍 *Location*
• *IP*: `{escape_markdown_user(ip)}`
• *Country*: {escape_markdown_user(country)}
• *Region*: {escape_markdown_user(region)}
• *City*: {escape_markdown_user(city)}
• *ZIP*: {escape_markdown_user(zip)}
• *Timezone*: {escape_markdown_user(timezone)}
• *Coords*: {escape_markdown_user(coords)}

📡 *Network*
• *ISP*: {escape_markdown_user(isp)}
• *Org*: {escape_markdown_user(org)}
• *AS*: {escape_markdown_user(asn)}

🛡 *Security*
• *Proxy/VPN*: {proxy_vpn}
• *Hosting/DC*: {hosting}"""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🌐 Lookup Another",
            "callback_data": "ip_lookup"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "tools"
        }
        ]
    ]
    }
        await message.answer(msg, parse_mode="MarkdownV2", reply_markup=keyboard)
    except:
        if number[0] != '+':
            number = '+'+number
        msg = fr"""❌ Invalid IP or lookup failed."""
        keyboard = {
    "inline_keyboard": [
        [
        {
            "text": "🔄 Try Again",
            "callback_data": "ip_lookup"
        }
        ],
        [
        {
            "text": "⬅ Back",
            "callback_data": "tools"
        }
        ]
    ]
    }
        await message.answer(msg, reply_markup=keyboard)




    await state.clear()
