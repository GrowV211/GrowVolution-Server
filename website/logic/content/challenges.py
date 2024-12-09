from flask import request
from website.basic import render
from website.data import Content, Challenge, add_model, delete_model, get_challenges
from .content import get_post_html
from ..auth.verify import active_user
from markupsafe import Markup


def _get_challenges_html():
    challenges = ""
    user = active_user()

    for challenge in get_challenges():
        if challenge.accepted(user):
            continue

        edited = ' | (bearbeitet)' if challenge.edited else ''
        timestamp = f"{challenge.date()}, {challenge.time()} | @{challenge.creator.username}{edited}"
        challenges += render('basic/content/challenge.html', id=challenge.id,
                             category=challenge.get_category(), headline=challenge.headline,
                             content=challenge.get_content(), timestamp=timestamp, active=user is not None,
                             post_user=challenge.creator == user)

    return Markup(challenges)


def _handle_fetch():
    data = request.get_json()
    value = data.get('value')

    if value == 'focus':
        post = Content.query.filter_by(id=int(data.get('post'))).first()
        return get_post_html(post)

    elif value == 'accept':
        user = active_user()
        add_model(Challenge(user.id, int(data.get('post'))))
        return ''

    elif value == 'cancel':
        user = active_user()
        challenge = Challenge.query.filter_by(userID=user.id, contentID=int(data.get('post'))).first()
        delete_model(challenge)
        return ''

    return _get_challenges_html()


def handle_request():

    if request.is_json:
        return _handle_fetch()

    return render('basic/content/challenges.html', challenges=_get_challenges_html())