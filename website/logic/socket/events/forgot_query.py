from ...auth.forgot import handle_request
from ..manage import send_message


def handle_event(data):
    send_message('update', handle_request(data))
