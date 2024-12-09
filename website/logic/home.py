from flask import request
from sqlalchemy import not_
from website.basic import render
from website.data import User, Content
from .auth.verify import active_user
from .content.content import get_post_html
from markupsafe import Markup


EXCLUDED = [
    '🏅'.encode('unicode_escape').decode('ascii'),
    '🌍'.encode('unicode_escape').decode('ascii')
]


def _render_content(user):
    content = ""
    user_list = User.query.order_by(User.score.desc()).all()

    for usr in user_list:
        if user and usr.id == user.id:
            continue

        content_list = (Content.query.filter_by(creatorID=usr.id)
                        .filter(not_(Content.category.in_(EXCLUDED)))
                        .order_by(Content.likes.desc()))

        i = 0
        for post in content_list:
            if i == 3:
                break

            edited = ' | (bearbeitet)' if post.edited else ''
            timestamp = f"{post.date()}, {post.time()} | @{post.creator.username}{edited}"
            content += render('basic/content/post_public.html', id=post.id,
                              category=post.get_category(), headline=post.headline,
                              content=post.get_content(), timestamp=timestamp)
            i += 1

    return Markup(content)


def _handle_fetch(user):
    data = request.get_json()
    value = data.get('value')

    if value == 'focus':
        post = Content.query.filter_by(id=int(data.get('post'))).first()
        print(post.id)
        return get_post_html(post)

    return _render_content(user)



def handle_request():
    user = active_user()

    if request.is_json:
        return _handle_fetch(user)

    return render("basic/home.html", content=_render_content(user))