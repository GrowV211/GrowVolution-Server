from ..conversation.chat import get_chat
from website.data import User, Socket, mod_messages, admin_messages
from website.socket import send_update


def _empty_message_update():
    return {
        'type': 'messages'
    }


def update_user_messages(data):
    user = User.query.filter_by(username=data['user']).first()
    socket = Socket.query.filter_by(userID=user.id).first()

    if not socket:
        return

    msg_type = data['type']

    if msg_type == 'messages':
        target_user = data['chat_user']

        update = _empty_message_update()

        if socket.tab == 'chats':
            target_user = User.query.filter_by(username=target_user).first()
            chat = get_chat(user, target_user)

            update['user'] = target_user.username
            update['messages'] = user.get_unread_chat_messages(chat)
            update['last'] = chat.get_last_message_text(user)
            send_update(socket.id, 'update_messages', update)

        update = _empty_message_update()
        update['messages'] = user.get_unread_messages()
        send_update(socket.id, 'update_messages', update)

    elif msg_type == 'requests':
        send_update(socket.id, 'update_messages', {
            'type': msg_type,
            'messages': user.get_unread_requests()
        })


def _send_moderation_update(users, msg_type, messages):
    for user in users:
        socket = Socket.query.filter_by(userID=user.id).first()
        if socket:
            send_update(socket.id, 'update_messages', {
                'type': msg_type,
                'messages': messages
            })


def update_moderation_messages(data):
    msg_type = data['type']
    admins = User.query.filter_by(role='ADMIN').all()

    if msg_type == 'mod_msgs':
        mods = User.query.filter_by(role='MOD').all()
        _send_moderation_update(mods + admins, msg_type, mod_messages())

    elif msg_type == 'admin_msgs':
        _send_moderation_update(admins, msg_type, admin_messages())
