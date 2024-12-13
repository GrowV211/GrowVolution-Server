from website.basic import render
from website.data import User
from website.logic.account.user import user_attributes
from website.logic.auth.verify import active_user
from markupsafe import Markup


def _get_users_html(users, ui_user):
    from website.logic.account.relation import relation_attributes

    user_list = ""
    count = 0

    for user in users:
        if user == ui_user:
            continue

        elif count > 50:
            break

        user_list += render('basic/account/profile_list_element.html',
                            type='profile-picture', user=user_attributes(user, False),
                            username=user.username, relation=relation_attributes(ui_user, user) if ui_user else { 'active': False })

        count += 1

    return Markup(user_list)


def handle_search(data):
    user = active_user()
    value = data.get('value')
    db = data.get('database')

    if db == 'users':
        users = User.query.filter(User.username.like(f"%{value}%")).order_by(User.score.desc()).all()
        return _get_users_html(users, user)

    return ''



def handle_request():
    return render('basic/search.html')