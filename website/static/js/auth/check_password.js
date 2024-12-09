document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("auth")

    const psw = document.getElementById("psw-new")
    const hint = document.getElementById("hint")
    const psw1 = document.getElementById("psw-new1")
    const hint1 = document.getElementById("hint1")

    let matching = false

    const interval = setInterval(() => {
        if (psw.value.length < 8) {
            hint.style.display = "block"
            return
        }
        else {
            hint.style.display = "none"
        }

        if (psw.value !== psw1.value) {
            hint1.style.display = "block"
            matching = false
        }
        else {
            hint1.style.display = "none"
            matching = true
        }
    }, 1500)

    document.getElementById("submit").addEventListener("click", () => {
        if (matching) {
            const domain_parts = window.location.href.split('/')
            const code = domain_parts[domain_parts.length - 1]

            fetch(`/reset/${code}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({value: psw.value})
            }).then(res => res.text()).then(data => {
                form.innerHTML = data

                form.querySelectorAll("script").forEach(script => {
                    eval(script.innerText)
                })
            })
        }
    })
})