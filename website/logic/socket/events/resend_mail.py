from ...auth.resend import handle_request
from ..manage import send_message


def handle_event(pid):
    send_message('resend_info', handle_request(pid))