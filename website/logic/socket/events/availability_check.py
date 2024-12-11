from ...account.available import handle_request
from ..manage import send_message
from ....debugger import log


def handle_event(data):
    log('info', f"Availability check requested.")
    send_message('availability_response', handle_request(data))
    log('info', "Availability response sent.")
