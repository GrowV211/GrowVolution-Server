from flask import request, redirect
from website.basic import render, goto_login
from website.data import Journal, add_model
from ..auth.verify import active_user
from markupsafe import Markup

ATTR_MAP = {
    "question_1": "answer1",
    "question_2": "answer2",
    "question_3": "answer3",
    "question_4": "answer4",
    "question_5": "answer5",
}


def _render_answer(question, answer):
    html = render('basic/account/journal_answer.html',
                  question=question, answer=answer)
    return Markup(html)


def _render_entries(user):
    entries = ""

    progress = user.progress[0]
    questions = progress.active_questions()

    for entry in user.journal:
        answers = entry.active_answers()
        answers_html = ""

        for attr, value in questions.items():
            answers_html += _render_answer(value, answers[ATTR_MAP[attr]])

        timestamp = f"{entry.date()}, {entry.time()}"
        entries += render('basic/account/journal_entry.html',
                          answers=answers_html, timestamp=timestamp)

    return Markup(entries)


def _render_answer_form(attr, question):
    return render('basic/account/journal_answer_form.html',
                  attr=attr, question=question)


def _render_form(user):
    form = ""

    progress = user.progress[0]
    questions = progress.active_questions()

    for attr, value in questions.items():
        form += _render_answer_form(ATTR_MAP[attr], value)

    return Markup(form)


def _add_entry(user):
    add_model(Journal(user.id, **request.form))
    user.update_score(10)
    return _render_entries(user)


def handle_request():
    user = active_user()

    if not user:
        goto_login()

    if not user.progress:
        return redirect('/progress')

    if request.method == "POST":
        return _add_entry(user)

    return render('basic/account/journal.html',
                  journal_entries=_render_entries(user),
                  questions=_render_form(user))
