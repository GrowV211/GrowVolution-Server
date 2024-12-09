from flask import request, jsonify
from website.basic import render
from website.temporary import RESET, lifecycle, new_process, TEN_MINUTES
from website.messaging import send_reset_link
from website.data import User


def handle_request():
    data = request.get_json()
    value = data.get('value')

    if value == 'forgot':
        return render('auth/forgot.html')

    elif value == 'reset-link':
        email = data.get('data')
        user = User.query.filter_by(email=email).first()

        pid = new_process()
        code = send_reset_link(email, user.first)
        lifecycle(RESET, pid, (code, user.id), TEN_MINUTES)

        return jsonify(value=f'https://growvolution.org/notice/{pid}')

    elif value == 'login':
        return render('auth/login_form.html')
