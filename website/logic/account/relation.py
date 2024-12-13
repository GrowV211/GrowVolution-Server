from website.basic import render, goto_login
from website.data import Request, add_model, delete_model, User
from website.logic.auth.verify import active_user
from .user import render_profile, user_attributes
from ..updating.messages import update_user_messages
from markupsafe import Markup


def _get_request(requestor, receiver):
    return Request.query.filter_by(requestorID=requestor, receiverID=receiver).first()


def _delete_request(requestor, receiver):
    delete_model(_get_request(requestor, receiver))


def relation_attributes(ui_user, profile_user):
    active = False
    requested = False
    requestor = False

    if not ui_user:
        return {
            'active': active,
            'profile_view': False
        }

    if _get_request(profile_user.id, ui_user.id):
        requested = True

    elif _get_request(ui_user.id, profile_user.id):
        requested = True
        requestor = True

    elif profile_user in ui_user.relators:
        active = True


    return {
        'active': active,
        'requested': requested,
        'requestor': requestor,
        'profile_view': True
    }


def handle_relation(receiver, value, data, profile=False):
    requestor = active_user()

    if value == 'add':
        r = Request(requestor.id, receiver.id)
        add_model(r)

    elif value == 'cancel':
        _delete_request(requestor.id, receiver.id)

    elif value == 'accept':
        _delete_request(receiver.id, requestor.id)

        requestor.add_relator(receiver)
        receiver.add_relator(requestor)

    elif value == 'deny':
        _delete_request(receiver.id, requestor.id)

    elif value == 'remove':
        requestor.remove_relator(receiver)
        receiver.remove_relator(requestor)

        from website.logic.conversation.chat import delete_chat
        delete_chat(requestor, receiver)

    update_user_messages({
        'user': receiver.username,
        'type': 'requests',
    })
    update_user_messages({
        'user': requestor.username,
        'type': 'requests',
    })

    if profile:
        return render_profile(receiver, True, False)
    elif data.get('breakpoint'):
        return '', 200

    data['value'] = data.get('container')
    return handle_interaction(data)


def _get_relations_html(user):
    relations = ""

    for relator in user.relators:
        relations += render('basic/account/profile_list_element.html',
                            type='profile-picture', user=user_attributes(relator, False),
                            username=relator.username, relation=relation_attributes(user, relator))

    return Markup(relations)


def _get_requests_html(user):
    requests = ""

    for r in user.requests_in:
        requestor = r.requestor
        r.set_read()
        requests += render('basic/account/profile_list_element.html',
                            type='profile-picture', user=user_attributes(requestor, False),
                            username=requestor.username, relation=relation_attributes(user, requestor))

    return Markup(requests)


def _get_pending_html(user):
    requests = ""

    for r in user.requests_out:
        requested = r.receiver
        requests += render('basic/account/profile_list_element.html',
                            type='profile-picture', user=user_attributes(requested, False),
                            username=requested.username, relation=relation_attributes(user, requested))

    return Markup(requests)


def handle_interaction(data):
    user = active_user()
    value = data.get('value')

    if value == 'active':
        return _get_relations_html(user)

    elif value == 'requested':
        return _get_requests_html(user)

    elif value == 'pending':
        return _get_pending_html(user)

    else:
        receiver = User.query.filter_by(username=data.get('receiver')).first()
        return handle_relation(receiver, value, data)


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    return render('basic/account/relation/relations.html',
                  relations=_get_relations_html(user))
