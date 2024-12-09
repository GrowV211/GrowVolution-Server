from flask import request, jsonify
from ..auth.verify import active_user
from ..conversation.chat import get_chat
from website.data import User, mod_messages, admin_messages


def handle_fetch():
    data = request.get_json()
    value = data.get('value')
    user = active_user()

    if not user:
        return ''

    if value == 'messages':
        target_user = data.get('chat_user')

        if target_user:
            target_user = User.query.filter_by(username=target_user).first()
            chat = get_chat(user, target_user)

            return jsonify({
                'messages': user.get_unread_chat_messages(chat),
                'last_message': chat.get_last_message_text(user)
            })

        return jsonify({'messages': user.get_unread_messages()})

    elif value == 'requests':
        return jsonify({'requests': user.get_unread_requests()})

    elif value == 'mod_msgs':
        return jsonify({'mod_msgs': mod_messages()})

    elif value == 'admin_msgs':
        return jsonify({'admin_msgs': admin_messages()})

    return '', 502