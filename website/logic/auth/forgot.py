from website.basic import render
from website.temporary import RESET, lifecycle, new_process, TEN_MINUTES
from website.mailservice import send_reset_link
from website.data import User
from markupsafe import Markup

def handle_request(data):
    value = data.get('value')

    if value == 'forgot':
        return {
            'value': 'html',
            'html': Markup(render('auth/forgot.html')),
            'type': 'forgot'
        }

    elif value == 'reset-link':
        email = data.get('data')
        user = User.query.filter_by(email=email).first()

        pid = new_process()
        code = send_reset_link(email, user.first)
        lifecycle(RESET, pid, (code, user.id), TEN_MINUTES)

        return {
            'value': 'url',
            'url': f'https://growvolution.org/notice/{pid}'
        }
