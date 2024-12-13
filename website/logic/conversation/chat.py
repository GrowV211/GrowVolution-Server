from website.basic import render
from website.data import Chat, add_model, delete_model
from markupsafe import Markup


def _render_date(date):
    return render('basic/conversation/message_date.html', date=date)


def render_message(direction, message):
    return render('basic/conversation/chat_message.html', direction=direction,
                  username=message.sender.username, message=message.get_content(), time=message.time())


def get_chat_html(chat, receiver):
    chat_html = ""
    current_date = None

    for msg in chat.messages:
        date = msg.date()

        if not current_date or date != current_date:
            current_date = date
            chat_html += _render_date(date)

        if msg.sender != receiver:
            direction = 'sent'
        else:
            direction = 'received'
            msg.set_read()

        chat_html += render_message(direction, msg)

    return Markup(chat_html)


def _get_chat(user, receiver):
    for c in user.chats:
        if receiver in c.participants:
            return c

    return None


def get_chat(user, receiver):
    chat = _get_chat(user, receiver)

    if not chat:
        chat = Chat()
        chat.participants.append(user)
        chat.participants.append(receiver)
        add_model(chat)

    return chat


def delete_chat(user, receiver):
    chat = _get_chat(user, receiver)

    if chat:
        delete_model(chat)


def render_chat(receiver, receiver_attributes, chat):
    return render('basic/conversation/chat_inner.html', type='chat-user', user=receiver_attributes,
                  name=receiver.name(), username=receiver.username, chat=get_chat_html(chat, receiver))
