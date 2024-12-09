from flask import request, flash, redirect
from website.basic import render, goto_login
from ..auth.verify import active_user


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    elif not user.is_admin():
        flash("Zugriff verweigert!", 'danger')
        return redirect('/')

    return render('basic/moderation/admin_panel.html')