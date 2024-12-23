from ....data import User
from ..manage import send_message
from ...auth.verify import active_session
from ...account.user import handle_interaction


def handle_event(data):
    session = active_session()
    user = User.query.filter_by(username=session.tab).first()

    send_message('update', handle_interaction(user, user == session.user, data))
