let form

async function updateForm(value, data = null) {
    const res = await fetch('/auth/forgot-password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({value: value, data: data})
    })

    if (res.headers.get('Content-Type').includes('application/json')) {
        const json = await res.json()
        const url = json['value']

        if (url)
            window.location = url
    } else {
        form.innerHTML = await res.text()

        if (value === 'login') {
            init()
            return
        }

        form.querySelectorAll("script").forEach(script => {
            eval(script.innerText)
        })
    }
}

function init() {
    form = document.getElementById("auth")
    const show_hide_btn = document.getElementById("show_hide");
    const password = document.getElementById("pass");

    show_hide_btn.addEventListener("click", function (e) {
        if (password.type === "password") {
         password.type = 'text';
         show_hide_btn.textContent = 'verstecken';
        } else {
            password.type = 'password';
            show_hide_btn.textContent = 'anzeigen';
        }
    });

    document.querySelectorAll("#help").forEach((help) => {
        help.addEventListener("click", () => {
            updateForm('forgot')
        })
    })
}

document.addEventListener("DOMContentLoaded", init);