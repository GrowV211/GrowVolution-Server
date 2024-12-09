from flask import render_template, flash, redirect
from markupsafe import Markup
from .data import mod_messages, admin_messages
from .logic.auth.verify import active_user


def render(template, **kwargs):
    user = active_user()

    unread_messages = user.get_unread_messages() if user else None
    unread_requests = user.get_unread_requests() if user else None

    mod_msgs = mod_messages() if user and (user.is_admin() or user.is_mod()) else None
    admin_msgs = admin_messages() if user and user.is_admin() else None

    return render_template(template, user_nav=True if user else False,
                           role=user.role if user else None,
                           unread_messages=unread_messages,
                           unread_requests=unread_requests,
                           mod_messages=mod_msgs,
                           admin_messages=admin_msgs, **kwargs)


def render_404():
    return render('404.html'), 404


def render_with_flash(template, message, category, **kwargs):
    flash(Markup(message), category)
    return render(template, **kwargs)


def goto_login():
    return redirect('/login')
