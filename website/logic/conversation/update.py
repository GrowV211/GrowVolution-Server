from website.data import Message, User, add_model, Session
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
    message = Message(sender.id, content, chat.id)
    add_model(message)

    chatroom = Session.query.filter(
        Session.chatID == chat.id,
        Session.sid != socket
    ).first()
    updated = False

    if chatroom:
        from ..socket.manage import send_message
        send_message('update_chat', Markup(render_message('received', message)), chatroom.socketID)
        message.set_read()
        updated = True


    if not updated:
        from ..updating.messages import update_user_messages
        update_user_messages({
            'type': 'messages',
            'user': receiver.username,
            'chat_user': sender.username
        })

    return Markup(render_message('sent', message))
