from flask import request, redirect
from website.basic import render,render_with_flash
from .verify import captcha_check
from website.data import User, add_model
from website.mailservice import send_confirm_mail
from website.temporary import lifecycle, new_process, TEN_MINUTES, CONFIRM
import random


def _confirm(model):
    add_model(model)
    return render('auth/signup_confirmed.html', email=model.email)


def _random_bg():
    hex_colors = [
        "#FFB6C1",  # Light Pink
        "#FFD700",  # Gold
        "#ADFF2F",  # Green Yellow
        "#87CEEB",  # Sky Blue
        "#FF69B4",  # Hot Pink
        "#FFA07A",  # Light Salmon
        "#FF6347",  # Tomato
        "#40E0D0",  # Turquoise
        "#EE82EE",  # Violet
        "#98FB98",  # Pale Green
        "#FFDAB9",  # Peach Puff
        "#E6E6FA",  # Lavender
        "#F08080",  # Light Coral
        "#FA8072",  # Salmon
        "#FF4500",  # Orange Red
        "#DA70D6",  # Orchid
        "#BA55D3",  # Medium Orchid
        "#7B68EE",  # Medium Slate Blue
        "#00FA9A",  # Medium Spring Green
        "#48D1CC"  # Medium Turquoise
    ]
    return random.choice(hex_colors)


def handle_request():
    template = 'auth/signup.html'

    if request.method == "POST":

        check = captcha_check()

        if check:
            return render_with_flash(template, check, 'danger')

        psw = request.form.get('psw')

        if not psw:
            return render_with_flash(template, "Dem Server wurde ein leeres Passwort übergeben!", "danger")

        first = request.form.get('first')
        user = request.form.get('user')
        email = request.form.get('email')

        user_model = User(first, request.form.get('last'), user, email, psw, _random_bg())

        pid = new_process()
        code = send_confirm_mail(email, first)

        lifecycle(CONFIRM, pid, (code, _confirm, user_model), TEN_MINUTES)

        return redirect(f'/notice/{pid}')

    else:
        return render('auth/signup.html')
