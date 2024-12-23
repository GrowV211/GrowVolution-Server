from flask import Blueprint, redirect
from . import ALL_METHODS, LIMITER
from .logic.auth import login as lin, signup as s, confirm as c, notice as n, reset as r, forgot

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=ALL_METHODS)
@LIMITER.limit("3 per minute")
def login():
    return lin.handle_request()


@auth.route('/logout')
def logout():
    return redirect('/')


@auth.route('/signup', methods=ALL_METHODS)
@LIMITER.limit("3 per minute")
def signup():
    return s.handle_request()


@auth.route('/notice/<pid>', methods=ALL_METHODS)
def notice(pid):
    return n.handle_request(pid)


@auth.route('/confirm/<code>')
def confirm(code):
    return c.handle_request(code)


@auth.route('/reset/<code>', methods=ALL_METHODS)
def reset(code):
    return r.handle_request(code)


@auth.route('/forgot-password', methods=ALL_METHODS)
def forgot_password():
    return forgot.handle_request()
