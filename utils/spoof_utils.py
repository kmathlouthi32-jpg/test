from config import get_spoofing, get_spoofing_services, get_servies

def check_spoof(spoof_number, service_name, name):
    if name.upper() in get_spoofing_services():
        return 'Name Found'
    try:
        service_place = get_spoofing_services().index(service_name.upper())
    except ValueError:
        if spoof_number == '+12104735470':
            return True
        else:
            return 'service not found'
    
    try:
        spoof_place = get_spoofing().index(spoof_number)
    except ValueError:
        return 'number not found'

    
    return spoof_place == service_place

def get_spoofer_number(service_name):
    return get_spoofing()[get_spoofing_services().index(service_name.upper())]

def get_service_name(service_name):
        return service_name.lower()

def get_service_name_bynum(num):
    if num == '+12104735470':
        return 'VIP spoof'
    return get_servies()[get_spoofing().index(num)]
