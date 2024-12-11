from ...auth.resend import handle_request
from ..manage import send_message
from ....debugger import log


def handle_event(pid):
    log('info', "Confirm mail resend requested.")
    send_message('resend_info', handle_request(pid))
    log('info', "Resend info sent.")