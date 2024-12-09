from website.basic import render_404
from website.temporary import CONFIRM, clear


def handle_request(code):
    for k, v in CONFIRM.items():
        if v[0] == code:
            clear(k)
            return v[1](v[2])

    return render_404()
