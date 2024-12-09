from flask import request, flash, redirect
from website.basic import render, goto_login
from website.data import get_challenges, Proof, delete_model
from ..auth.verify import active_user
from markupsafe import Markup


def _render_unmanaged_challenges(user):
    challenges = ""

    for challenge in get_challenges(managed=False):
        if challenge.creator == user:
            continue

        challenges += render('basic/moderation/challenge_manage.html', id=challenge.id,
                             headline=challenge.headline, content=challenge.get_content())

    return Markup(challenges)


def _render_proves(user):
    proves = ""

    for proof in Proof.query.all():
        #if proof.challenge.user == user:
        #    continue

        challenge = proof.challenge.content
        proves += render('basic/moderation/proof_manage.html', id=proof.id,
                         headline=challenge.headline, content=challenge.get_content(),
                         proves=proof.get_proves_html())

    return Markup(proves)


def _get_proof(target):
    return Proof.query.filter_by(id=target).first()


def _delete_proof(proof):
    proof.delete_files()
    delete_model(proof)


def _handle_fetch(user):
    data = request.get_json()
    value = data.get('value')

    if value == "challenges":
        return _render_unmanaged_challenges(user)

    elif value == 'provable':
        challenge = get_challenges(id=int(data.get('target')))[0]
        challenge.set_provable()
        challenge.set_managed()

        return _render_unmanaged_challenges(user)

    elif value == 'unprovable':
        challenge = get_challenges(id=int(data.get('target')))[0]
        challenge.set_managed()

        return _render_unmanaged_challenges(user)

    elif value == 'proves':
        return _render_proves(user)

    elif value == 'confirm':
        proof = _get_proof(int(data.get('target')))
        proof.challenge.user.update_score(30)
        proof.challenge.set_proved()
        proof.challenge.set_managed()
        _delete_proof(proof)
        return _render_proves(user)

    elif value == 'deny':
        proof = _get_proof(int(data.get('target')))
        proof.challenge.set_managed()
        _delete_proof(proof)
        return _render_proves(user)

    elif value == 'reports':
        return ''


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    elif not user.is_admin() and not user.is_mod():
        flash("Zugriff verweigert!", 'danger')
        return redirect('/')

    if request.is_json:
        return _handle_fetch(user)

    return render('basic/moderation/mod_panel.html', challenges=_render_unmanaged_challenges(user))