from ..conversation.chat import get_chat
from website.data import User, Session, mod_messages, admin_messages
from ..socket.manage import send_message


def _empty_message_update():
    return {
        'type': 'messages'
    }


def update_user_messages(data):
    user = User.query.filter_by(username=data['user']).first()
    sessions = Session.query.filter_by(userID=user.id).all()

    if not sessions:
        return

    msg_type = data['type']

    if msg_type == 'messages':
        target_user = data['chat_user']

        for session in sessions:
            update = _empty_message_update()

            if session.tab == 'chats':
                target_user = User.query.filter_by(username=target_user).first()
                chat = get_chat(user, target_user)

                update['user'] = target_user.username
                update['messages'] = user.get_unread_chat_messages(chat)
                update['last'] = chat.get_last_message_text(user)
                send_message('update_messages', update, session.sid)
            else:
                update['messages'] = user.get_unread_messages()
                send_message('update_messages', update, session.sid)

    elif msg_type == 'requests':
        for session in sessions:
            if session.sid:
                send_message('update_messages', {
                    'type': msg_type,
                    'messages': user.get_unread_requests()
                }, session.sid)


def _send_moderation_update(users, msg_type, messages):
    for user in users:
        sessions = Session.query.filter_by(userID=user.id).all()
        if sessions:
            for session in sessions:
                send_message('update_messages', {
                    'type': msg_type,
                    'messages': messages
                }, session.sid)


def update_moderation_messages(data):
    msg_type = data['type']
    admins = User.query.filter_by(role='ADMIN').all()

    if msg_type == 'mod_msgs':
        mods = User.query.filter_by(role='MOD').all()
        _send_moderation_update(mods + admins, msg_type, mod_messages())

    elif msg_type == 'admin_msgs':
        _send_moderation_update(admins, msg_type, admin_messages())
