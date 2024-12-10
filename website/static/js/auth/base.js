let form

function init() {
    form = document.getElementById("auth")
    const show_hide_btn = document.getElementById("show_hide");
    const password = document.getElementById("pass");
    const help = document.getElementById("help")

    function onUpdateEvent(data) {
        const value = data.value

        if (value === 'html') {
            form.innerHTML = data.html

            if (data.type === 'login') {
                init()
                return
            }

            form.querySelectorAll("script").forEach(script => {
                eval(script.innerText)
            })
        } else {
            window.location = data.url
        }
    }

    updateEventHandler = onUpdateEvent

    show_hide_btn.addEventListener("click", function (e) {
        if (password.type === "password") {
         password.type = 'text';
         show_hide_btn.textContent = 'verstecken';
        } else {
            password.type = 'password';
            show_hide_btn.textContent = 'anzeigen';
        }
    });

    if (help) {
        setTab('login')
        help.addEventListener("click", () => {
            forgotQuery({ value: 'forgot' })
        })
    }
}

document.addEventListener("DOMContentLoaded", init);