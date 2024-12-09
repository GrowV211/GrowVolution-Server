from flask import request
from website.basic import render, goto_login
from website.data import Content, Comment, Like, add_model, delete_model
from website.logic.auth.verify import active_user
from markupsafe import Markup


def _get_answers_html(comment):
    from website.logic.account.user import user_attributes
    answers = ""
    user = active_user()
    answer_list = Comment.query.filter_by(commentID=comment.id).order_by(Comment.likes.desc()).all()

    for answer in answer_list:
        edited = ' (bearbeitet)' if answer.edited else ''
        timestamp = f"{answer.date()}, {answer.time()}{edited}"
        answers += render('basic/content/answer.html', id=answer.id, type='comment-user',
                          user=user_attributes(answer.writer, False),
                          username=answer.writer.username, content=answer.content,
                          timestamp=timestamp, comment_user=answer.writer == user,
                          active=user is not None, liked=user.has_liked(comment=answer.id) if user else None)

    return Markup(answers)


def get_comments_html(post):
    from website.logic.account.user import user_attributes
    comments = ""
    user = active_user()
    comment_list = Comment.query.filter_by(contentID=post.id).order_by(Comment.likes.desc()).all()

    for comment in comment_list:
        if comment.is_reply():
            continue
        edited = ' (bearbeitet)' if comment.edited else ''
        timestamp = f"{comment.date()}, {comment.time()}{edited}"
        comments += render('basic/content/comment.html', id=comment.id, type='comment-user',
                           user=user_attributes(comment.writer, False),
                           username=comment.writer.username, content=comment.content,
                           timestamp=timestamp, comment_user=comment.writer == user,
                           answers=_get_answers_html(comment), active=user is not None,
                           liked=user.has_liked(comment=comment.id) if user else None)

    return Markup(comments)


def _get_content(target_id):
    return Content.query.filter_by(id=target_id).first()


def _get_comment(target_id):
    return Comment.query.filter_by(id=target_id).first()


def _handle_post(user):
    data = request.get_json()
    target_id = int(data.get('id'))
    answer_id = data.get('answerTo')

    target = _get_content(target_id)
    target_comment = None

    if answer_id:
        target_comment = _get_comment(int(answer_id))

        if target_comment.is_reply():
            target_comment = target_comment.parent

    if not target:
        return '', 502

    comment = Comment(user.id, target.id, request.get_json().get('value'), target_comment.id if target_comment else None)
    add_model(comment)

    return get_comments_html(target)


def _handle_update():
    data = request.get_json()
    target_id = int(data.get('id'))
    value = data.get('value')

    target = _get_comment(target_id)
    parent = target.parent if target.is_reply() else None
    post = target.post

    if value == 'delete':
        for answer in target.answers:
            delete_model(answer)
        delete_model(target)

    elif value == 'edit':
        target.edit(data.get('content'))

    elif value == 'like':
        target.like()
        like = Like(active_user().id, comment=target.id)
        add_model(like)
        target.writer.update_score(1)

        return ''

    elif value == 'unlike':
        target.unlike()
        like = Like.query.filter_by(userID=active_user().id, commentID=target.id).first()
        delete_model(like)
        target.writer.update_score(-1)

        return ''

    else:
        return '', 502

    if target.is_reply():
        return _get_answers_html(parent)
    else:
        return get_comments_html(post)


def handle_request(cmd):
    user = active_user()

    if not user:
        return goto_login()

    if request.is_json:
        if cmd == 'post':
            return _handle_post(user)
        else:
            return _handle_update()

    return ''
