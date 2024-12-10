from flask import Blueprint
from . import ALL_METHODS
from .basic import render, render_404
from .logic.account import user, relation, progress as p, journal as j, accepted as a, edit as e
from .logic.conversation import chats
from .logic.content import challenges as c
from .logic.moderation import mod, admin
from .logic.teams import teams as t
from .logic import search as s, ranking as r, home

views = Blueprint('views', __name__)


@views.route('/', methods=ALL_METHODS)
def index():
    return home.handle_request()


@views.route('/impressum')
def impressum():
    return render('basic/impressum.html')


@views.route('/privacy')
def privacy():
    return render('basic/privacy.html')


@views.route('/guidelines')
def guidelines():
    return render('basic/guidelines.html')


@views.route('/about')
def about():
    return render('basic/about.html')


@views.route('/search', methods=ALL_METHODS)
def search():
    return s.handle_request()


@views.route('/user/<username>', methods=ALL_METHODS)
def profile(username):
    return user.handle_request(username)


@views.route('/user', methods=ALL_METHODS)
def active_profile():
    return user.handle_request(None)


@views.route('/conversations', methods=ALL_METHODS)
def conversations():
    return chats.handle_request()


@views.route('/relations', methods=ALL_METHODS)
def relations():
    return relation.handle_request()


@views.route('/challenges', methods=ALL_METHODS)
def challenges():
    return c.handle_request()


@views.route('/accepted', methods=ALL_METHODS)
def accepted():
    return a.handle_request()


@views.route('/mod-panel', methods=ALL_METHODS)
def mod_panel():
    return mod.handle_request()


@views.route('/admin-panel', methods=ALL_METHODS)
def admin_panel():
    return admin.handle_request()


@views.route('/progress', methods=ALL_METHODS)
def progress():
    return p.handle_request()


@views.route('/teams', methods=ALL_METHODS)
def teams():
    return t.handle_request()


@views.route('/journal', methods=ALL_METHODS)
def journal():
    return j.handle_request()


@views.route('/ranking', methods=ALL_METHODS)
def ranking():
    return r.handle_request()


@views.route('/<path:path>')
def not_found(path):
    return render_404()


# Fetch Only
@views.route('/edit', methods=['POST'])
def edit():
    return e.handle_request()
