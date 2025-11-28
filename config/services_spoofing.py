# bot/services.py
# Services & spoofing lists. Use tuples (immutable) to reduce accidental modification.
def get_servies():
    return (
    "amazon", "google", "facebook", "twitter", "uber",
"chasebank", "bankofamerica", "wellsfargo", "usbank", "truistbank",
"citibank", "pncbank", "capitalone", "tdbank", "hsbcbankusa",
"chasebank", "wellsfargo", "usbank", "truistbank",
"citizens", "pncbank", "capitalone", "tdbank", "hsbcbankusa",
"usaa", "americanexpress", "charlesschwab", "ikea", "ashleyfurniture",
"wayfair", "slumberlandfurniture", "oneplus", "sonymobile", "nokiahmdglobal",
"htc", "blackberry", "googlepixelphones", "jeep"

    )

def get_spoofing():
    return (
        "12062664001",
        "16502530000",
        "16505434800",
        "14153650704",
        "14156896300",
        "12122706000",
        "13157244022",
        "19258257600",
        "15034019991",
        "19109148250",
        "12106773775",
        "14123034000",
        "17038772000",
        "18567519000",
        "17168417212",
        "12122706000",
        "19258257600",
        "15034019991",
        "19109148250",
        "12106773775",
        "14123034000",
        "17038772000",
        "18567519000",
        "17168417212",
        "12105318722",
        "13363931111",
        "14125575000",
        "18888884532",
        "18664363393",
        "18779243247",
        "18889575862",
        "18884880033",
        "18557669669",
        "18889986654",
        "18666179347",
        "18772552373",
        "18444006348",
        "18777442646"
    )

def get_spoofing_services():
    return (
        "AMAZON", "GOOGLESUPPORT", "FACEBOOKSUPPORT", "TWITTERSUPPORT", "UBERSUPPORT",
        "CHASEBANK", "BANKOFAMERICA", "WELLSFARGO", "USBANK", "TRUISTBANK",
        "CITIZENS", "PNCBANK", "CAPITALONE", "TDBANK", "HSBCBANKUSA",
        "CHASEBANK", "BANKOFAMERICA", "WELLSFARGO", "USBANK", "TRUISTBANK",
        "CITIBANK", "PNCBANK", "CAPITALONE", "TDBANK", "HSBCBANKUSA",
        "USAA", "AMERICANEXPRESS", "CHARLESSCHWAB", "IKEA", "ASHLEYFURNITURE",
        "WAYFAIR", "SLUMBERLANDFURNITURE", "ONEPLUS", "SONYMOBILE", "NOKIAHMDGLOBAL",
        "HTC", "BLACKBERRY", "GOOGLEPIXELPHONES", "JEEP", 'CREDITCARD'
    )

def get_pre_spoofing_services():
    return (
    "PAYPAL",
    "VENMO",
    "APPLEPAY",
    "COINBASE",
    "MICROSOFT",
    "AMAZON",
    "QUADPAY",
    "CASHAPP",
    "CITIZENS",
    "MARCUS",
    "CARRIER",
    "CREDITCARD",
    "SSN"
)

def get_pre_spoofing_numbers():
    return ("18324142447", "16124610294", "14843823142", "18327565740",
        "12107652610", "12062664001", "13173629695", "12104523112", "12106773775", "14843506824",
        "18329335811", '18322268948','13172198058')
# Template builder for the spoof message.
def spoof_message():
    # build on-demand so the string is created only when needed
    n = get_spoofing()
    return fr"""☎️ 》 LIST OF CALLER ID :
AMAZON: 12062664001
Google Support: 16502530000
Facebook Support: 16505434800
Twitter Support: 14153650704
Uber Support: 14156896300
Chase Bank: 12122706000
Bank of America: 13157244022
Wells Fargo: 19258257600
U.S. Bank: 15034019991
Truist Bank: 19109148250
Citibank: 12106773775
PNC Bank: 14123034000
Capital One: 17038772000
TD Bank: 18567519000
HSBC Bank USA: 17168417212
Regions Bank: 12053372200
USAA: 12105318722
American Express: 13363931111
Charles Schwab: 14125575000
IKEA: 18888884532
Ashley Furniture: 18664363393
Wayfair: 18779243247
Slumberland Furniture: 18889575862
OnePlus: 18884880033
Sony Mobile: 18557669669
Nokia (HMD Global): 18889986654
HTC: 18666179347
BlackBerry: 18772552373
Google (Pixel phones): 18444006348
Jeep: 18777442646"""
