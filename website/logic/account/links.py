from flask import request, jsonify
from website.basic import render, goto_login
from website.data import Link, add_model
from website.logic.auth.verify import active_user
from markupsafe import Markup


def _get_links_html(user):
    links = ""
    socials = ""
    current = user == active_user()

    for link in user.links:
        if not link.is_social():
            links += render('basic/content/link.html',
                            link=link.link, titel=link.titel,
                            link_user=current)
        else:
            socials += render('basic/content/social.html',
                              link=link.link, social=link.social,
                              link_user=current)

    return {
        'links': Markup(links),
        'socials': Markup(socials)
    }


def handle_fetch():
    user = active_user()

    if not user:
        return goto_login()

    if request.method == 'POST':
        data = request.form
        link_type = data.get('type')

        if link_type == 'standard':
            add_model(Link(user.id, data.get('link'), data.get('titel')))
        else:
            add_model(Link(user.id, data.get('link'), data.get('titel'), data.get('social')))

    return jsonify(_get_links_html(user))


def handle_request(user, current):
    links = _get_links_html(user)

    if current:
        template = 'basic/content/links_edit.html'
    else:
        template = 'basic/content/links.html'

    return render(template, socials=links['socials'], links=links['links'])
