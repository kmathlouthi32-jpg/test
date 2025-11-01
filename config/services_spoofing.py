# bot/services.py
# Services & spoofing lists. Use tuples (immutable) to reduce accidental modification.
def get_servies():
    return (
    "amazon", "google", "facebook", "twitter support", "applepay", "microsoft",
    "paypal", "venmo", "cashapp", "coinbase", "quadpay",
    "chase bank", "bank of america", "wells fargo", "u.s. bank", "truist bank",
    "citibank", "pnc bank", "capital one", "td bank", "hsbc bank usa",
    "american express", "citizens", "marcus", "carrier"
    )

def get_spoofing():
    return (
        "+18327565740", "+12105055926", "+18326896767", "+13177171763", "+13176199482",
        "+14842898053", "+16026779146", "+13177379548", "+14848323135", "+15863273508",
        "+16028773238", "+18322268948", "+14844782412", "+16027404712", "+12108101186",
        "+18324353797", "+15863060374", "+13173629695", "+12108481328", "+16025962733",
        "+15864419789", "+18323357355", "+16127078744", "+18324361309", "+16128426925"
    )

def get_spoofing_services():
    return (
        "AMAZON", "GOOGLE", "FACEBOOK", "TWITTERSUPPORT", "APPLEPAY", "MICROSOFT",
        "PAYPAL", "VENMO", "CASHAPP", "COINBASE", "QUADPAY",
        "CHASEBANK", "BANKOFAMERICA", "WELLSFARGO", "USBANK", "TRUISTBANK",
        "CITIBANK", "PNCBANK", "CAPITALONE", "TDBANK", "HSBCBANKUSA",
        "AMERICANEXPRESS", "CITIZENS", "MARCUS", "CARRIER"
    )

# Template builder for the spoof message.
def spoof_message():
    # build on-demand so the string is created only when needed
    n = get_spoofing()
    return fr"""📞 *Spoof Numbers*

🛒 *Retail & Tech Services*
 • *Amazon* – `{n[0]}`
 • *Google* – `{n[1]}`
 • *Facebook* – `{n[2]}`
 • *Twitter Support* – `{n[3]}`
 • *Apple Pay* – `{n[4]}`
 • *Microsoft* – `{n[5]}`
 • *PayPal* – `{n[6]}`
 • *Venmo* – `{n[7]}`
 • *CashApp* – `{n[8]}`
 • *Coinbase* – `{n[9]}`
 • *Quadpay* – `{n[10]}`

🏦 *Banking & Financial Services*
 • *Chase Bank* – `{n[11]}`
 • *Bank of America* – `{n[12]}`
 • *Wells Fargo* – `{n[13]}`
 • *U\.S Bank* – `{n[14]}`
 • *Truist Bank* – `{n[15]}`
 • *Citibank* – `{n[16]}`
 • *PNC Bank* – `{n[17]}`
 • *Capital One* – `{n[18]}`
 • *TD Bank* – `{n[19]}`
 • *HSBC Bank USA* – `{n[20]}`
 • *American Express* – `{n[21]}`
 • *Citizens Bank* – `{n[22]}`
 • *Marcus \(Goldman Sachs\)* – `{n[23]}`

📦 *Other Services*
 • *Carrier* – `{n[24]}`"""
