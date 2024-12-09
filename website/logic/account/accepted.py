from flask import request
from werkzeug.utils import secure_filename
from website.basic import render, goto_login
from website.data import Proof, PROOF_PATH, add_model
from ..auth.verify import active_user
from ..content.challenges import _handle_fetch as cancel
from markupsafe import Markup
from ...data import Challenge
import uuid


def _render_accepted_challenges(user):
    challenges = ""

    for challenge in user.challenges:
        post = challenge.content

        edited = ' | (bearbeitet)' if post.edited else ''
        timestamp = f"{post.date()}, {post.time()} | @{post.creator.username}{edited}"

        challenges += render('basic/content/challange_accepted.html', id=post.id,
                             headline=post.headline, category=post.get_category(), content=post.get_content(),
                             timestamp=timestamp, done=challenge.done, provable=post.provable)

    return Markup(challenges)


def _handle_fetch(user):
    if request.is_json:
        cancel()
        return _render_accepted_challenges(user)

    data = request.form
    challenge = Challenge.query.filter_by(userID=user.id, contentID=int(data.get('challenge'))).first()

    if data.get('no_evidence'):
        challenge.finish()
        return ''

    files = request.files.getlist('files')

    saved = {}
    i = 1
    for file in files:
        if file.filename:
            extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = secure_filename(f"{uuid.uuid4()}.{extension}")
            file.save(PROOF_PATH / unique_filename)
            saved[f'proof{str(i)}'] = unique_filename
            i += 1

    add_model(Proof(challenge.id, **saved))
    return ''


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    if request.method == 'POST':
        return _handle_fetch(user)

    return render('basic/account/accepted_challenges.html',
                  challenges=_render_accepted_challenges(user))
