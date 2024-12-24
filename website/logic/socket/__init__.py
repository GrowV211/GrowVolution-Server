from ...logging import S_EVENTS
from .events import (connect, back,
                     join_chatroom, availability_check, forgot_query,
                     chat_message, resend_mail, profile_interaction)
from ..account.edit import handle_edit, handle_reset_request, handle_delete
from ..search import handle_search
from ..content.content import handle_content_interaction
from ..auth.verify import active_session
from .manage import send_message


@S_EVENTS.on('connect')
def on_connect():
    connect.handle_event()


@S_EVENTS.on('disconnect')
def on_disconnect():
    active_session().set_socket(None)


@S_EVENTS.on('verify_session')
def on_verify_session():
    active_session().set_verified()


@S_EVENTS.on('back')
def on_back():
    back.handle_event()


@S_EVENTS.on('set_tab')
def on_set_tab(tab):
    session = active_session()
    if session:
        session.set_tab(tab)


@S_EVENTS.on('search')
def on_search(data):
    send_message('search_response', handle_search(data))


@S_EVENTS.on('availability_check')
def on_availability_check(data):
    availability_check.handle_event(data)


@S_EVENTS.on('forgot_query')
def on_forgot_query(data):
    forgot_query.handle_event(data)


@S_EVENTS.on('resend_mail')
def on_resend(pid):
    resend_mail.handle_event(pid)


@S_EVENTS.on('profile_interaction')
def on_profile_interaction(data):
    profile_interaction.handle_event(data)


@S_EVENTS.on('edit_profile')
def on_edit_profile(data):
    send_message('profile_update', handle_edit(data))


@S_EVENTS.on('reset_edit')
def on_reset_edit():
    send_message('edit_reset', handle_reset_request())


@S_EVENTS.on('delete_pp')
def on_pp_delete():
    send_message('pp_delete', handle_delete())


@S_EVENTS.on('relation_interaction')
def on_relation_interaction(data):
    from ..account.relation import handle_interaction
    send_message('relation_update', handle_interaction(data))


@S_EVENTS.on('join_chatroom')
def on_join_chatroom(username):
    join_chatroom.handle_event(username)


@S_EVENTS.on('chat_message')
def on_chat_message(data):
    chat_message.handle_event(data)


@S_EVENTS.on('content_interaction')
def on_content_interaction(data):
    send_message('content_interaction_response', handle_content_interaction(data))

