from flask import request, url_for, redirect
from website.basic import render, render_404, goto_login
from website.logic.content.content import render_create_view, get_content_html, get_post_html
from website.data import User, Content
from website.logic.auth.verify import active_user
from . import links
from datetime import datetime


EDITING = {}


def _image_source(src, timestamp):
    if timestamp:
        t = f"?t={datetime.now().timestamp()}"
    else:
        t = ''

    return f"{url_for('static', filename=f'img/usr/{src}')}{t}"


def user_attributes(user, img_timestamp):
    first = user.first
    last = user.last
    img = user.img

    usr = {'name': f"{first} {last}"}

    if img:
        usr['img_src'] = _image_source(img, img_timestamp)
        usr['img'] = img
    else:
        usr['img_src'] = None
        usr['initials'] = f"{first[0]}{last[0]}"
        usr['bg_color'] = user.alt_bg

    return usr


def render_profile(user, inner, current, img_timestamp = False):
    if inner:
        template = 'basic/account/profile_inner.html'
    else:
        template = 'basic/account/profile.html'

    request_has_active_user = active_user() is not None

    if request_has_active_user and not current:
        from .relation import relation_attributes
        relation = relation_attributes(active_user(), user)
    else:
        relation = None

    return render(template, username=user.username,
                  user=user_attributes(user, img_timestamp), info=user.info,
                  current=current, active=request_has_active_user, relation=relation,
                  content=get_content_html(user))


def handle_interaction(user, current, data):
    global EDITING
    value = data['value']

    if value == 'edit' and current:
        EDITING[user.id] = True

        from .edit import render_edit
        return render_edit(user, user_attributes(user, False))

    elif value == 'settings' and current:
        from .settings import render_settings
        return render_settings()

    elif value == 'new_post':
        return render_create_view()

    elif value == 'post':
        post = Content.query.filter_by(id=request.get_json().get('post')).first()
        return get_post_html(post)

    elif value == 'links':
        return links.handle_request(user, current)

    elif not current:
        from .relation import handle_relation
        return handle_relation(user, value)

    else:
        timestamp = False
        if current:
            timestamp = True if EDITING.get(user.id) else False
            EDITING[user.id] = False

        return render_profile(user, True, current, timestamp)


def handle_request(username):
    if username:
        user = User.query.filter_by(username=username).first()
        if user == active_user():
            return redirect('/user')
        current = False
    else:
        user = active_user()
        if not user:
            return goto_login()
        current = True

    if not user:
        return render_404()

    return render_profile(user, False, current)
