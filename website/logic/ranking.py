from website.basic import render
from website.data import User
from .account.user import user_attributes
from markupsafe import Markup


RANK_MAP = {
    1: "first",
    2: "second",
    3: "third",
}


def _get_rank_text(rank):
    return RANK_MAP.get(rank, 'place')


def _render_ranking_list():
    rank_list = ""
    user_list = User.query.order_by(User.score.desc()).all()
    rank = 1

    for user in user_list:
        rank_list += render('basic/rank_list_element.html',
                            user=user_attributes(user, False),
                            type='profile-picture', rank_text=_get_rank_text(rank),
                            rank=rank, username=user.username, score=user.score)
        rank += 1

    return Markup(rank_list)


def handle_request():
    return render('basic/ranking.html', ranking_list=_render_ranking_list())