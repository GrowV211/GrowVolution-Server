from ...account.available import handle_request
from ..manage import send_message


def handle_event(data):
    send_message('availability_response', handle_request(data))
