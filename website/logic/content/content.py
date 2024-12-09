from flask import request
from website.basic import render, goto_login
from website.data import Content, Like, add_model, delete_model
from website.logic.auth.verify import active_user
from .comment import get_comments_html
from markupsafe import Markup


def get_post_html(post):
    user = active_user()
    edited = ' | (bearbeitet)' if post.edited else ''
    timestamp = f"{post.date()}, {post.time()} | @{post.creator.username}{edited}"
    return render('basic/content/post.html', id=post.id, category=post.get_category_text(),
                  headline= post.headline, body=post.get_content(), timestamp=timestamp,
                  active=user is not None, post_user=post.creator == user, comments=get_comments_html(post),
                  challenge=post.is_challenge(), accepted=post.accepted(user),
                  liked=user.has_liked(post.id) if user else None)


def get_content_html(user):
    content = ""
    content_list = Content.query.filter_by(creatorID=user.id).order_by(Content.likes.desc()).all()

    for post in content_list:
        edited = ' (bearbeitet)' if post.edited else ''
        timestamp = f"{post.date()}, {post.time()}{edited}"
        content += render('basic/content/post_simple.html', id=post.id, category=post.get_category(),
                          headline=post.headline, body=post.get_content(), timestamp=timestamp)

    return Markup(content)


def render_create_view():
    return render('basic/content/create.html')


def _handle_fetch():
    data = request.get_json()
    value = data.get('value')
    post = Content.query.filter_by(id=int(data.get('id'))).first()

    if value == 'delete':
        for comment in post.comments:
            delete_model(comment)
        delete_model(post)

        return ''

    elif value == 'edit':
        post.edit(data.get('headline'), data.get('content'))

    elif value == 'like':
        post.like()
        add_model(Like(active_user().id, post.id))
        post.creator.update_score(1)

        return ''

    elif value == 'unlike':
        post.unlike()
        like = Like.query.filter_by(userID=active_user().id, contentID=post.id).first()
        delete_model(like)
        post.creator.update_score(-1)

        return ''

    return get_post_html(post)

def handle_request():
    user = active_user()

    if not user:
        return goto_login(), 500

    if request.is_json:
        return _handle_fetch()

    if request.method == "POST":
        new_post = Content(user.id, request.form['headline'], request.form['body'], request.form['category'])
        add_model(new_post)

        return '', 200

    return ''