from website.data import Message, ChatKey, User, add_model, Session
from website.logic.auth.verify import active_user
from .chat import get_chat, render_message
from markupsafe import Markup


def handle_request(data, socket):
    sender = active_user()
    receiver = User.query.filter_by(username=data['username']).first()

    if not sender or not receiver:
        return

    chat = get_chat(sender, receiver)
    content = data['content']

    key = ChatKey.query.filter_by(chatID=chat.id, userID=sender.id).first()
    chat_key = key.get_chat_key(sender.password[0].get_password(True)) # Skipping cause sender = active_user()

    message = Message(sender.id, content, chat.id, chat_key)
    add_model(message)

    chatroom = Session.query.filter(
        Session.chatID == chat.id,
        Session.sid != socket
    ).first()
    updated = False

    if chatroom:
        from ..socket.manage import send_message
        send_message('update_chat', Markup(render_message('received', message, chat_key)), chatroom.sid)
        message.set_read()
        updated = True


    if not updated:
        from ..updating.messages import update_user_messages
        update_user_messages({
            'type': 'messages',
            'user': receiver.username,
            'chat_user': sender.username
        })

    return Markup(render_message('sent', message, chat_key))
