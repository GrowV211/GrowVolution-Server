from flask import request
from website.data import Progress, add_model
from website.basic import render, goto_login
from ..auth.verify import active_user


def _create_progress(user):

    progress_data = {
        "userID": user.id,
        "goal": request.form.get("goal"),
        "body_current": request.form.get("body"),
        "mental_current": request.form.get("mental"),
        "relations_current": request.form.get("relations"),
        "personal_current": request.form.get("personal"),
        "financial_current": request.form.get("financial"),
        "career_current": request.form.get("career"),
        "spiritual_current": request.form.get("spiritual"),
        "body_future": request.form.get("body_future"),
        "mental_future": request.form.get("mental_future"),
        "relations_future": request.form.get("relations_future"),
        "personal_future": request.form.get("personal_future"),
        "financial_future": request.form.get("financial_future"),
        "career_future": request.form.get("career_future"),
        "spiritual_future": request.form.get("spiritual_future"),
        "question_1": request.form.get("q1"),
        "question_2": request.form.get("q2"),
        "question_3": request.form.get("q3"),
        "question_4": request.form.get("q4"),
        "question_5": request.form.get("q5"),
        "journal_time": request.form.get("journal_time"),
    }

    add_model(Progress(user.id, **progress_data))
    user.update_score(100)


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    if request.method == "POST":
        _create_progress(user)

    progress = Progress.query.filter_by(userID=user.id).first()

    if progress:
        return render(
            'basic/account/progress.html',
            goal=progress.goal,

            body_current=progress.body_current,
            mental_current=progress.mental_current,
            relations_current=progress.relations_current,
            personal_current=progress.personal_current,
            financial_current=progress.financial_current,
            career_current=progress.career_current,
            spiritual_current=progress.spiritual_current,

            body_future=progress.body_future,
            mental_future=progress.mental_future,
            relations_future=progress.relations_future,
            personal_future=progress.personal_future,
            financial_future=progress.financial_future,
            career_future=progress.career_future,
            spiritual_future=progress.spiritual_future
        )

    return render('basic/account/progress_first.html')