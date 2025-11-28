from .phone_utils import get_region_language, is_valid_phone_number
from .text_utils import escape_markdown, is_name_valid
from .payment_utils import get_wallet_message, check_subscription
from .spoof_utils import check_spoof, get_spoofer_number,get_service_name ,get_service_name_bynum
from .database import db
from .handlers_manager import get_user_cached, load_all_users, update_user_cache, is_new_user



