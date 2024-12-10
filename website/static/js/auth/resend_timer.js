document.addEventListener("DOMContentLoaded", function () {
    const resend = document.getElementById("resend")
    const hint = document.getElementById("hint")
    const resend_disabled = 'Du kannst diese Funktion in <span id="time"></span> Sekunden wieder nutzen.'

    let time = parseInt(document.getElementById("time").textContent)

    function update() {
        document.getElementById("time").textContent = time
    }

    function timer() {
        time--
        update()
        if(time <= 0) {
            hint.innerHTML = ''
            resend.disabled = false
            clearInterval(interval)
        }
    }

    function init_lock() {
        resend.disabled = true
        hint.innerHTML = resend_disabled
        update()
    }

    init_lock()

    let interval = setInterval(timer, 1000)

    function onResendInfo(lockTime) {
        time = lockTime
        init_lock()
        interval = setInterval(timer, 1000)
    }

    resendInfoEventHandler = onResendInfo

    resend.addEventListener("click", () => {
        const domain_parts = window.location.href.split('/')
        const pid = domain_parts[domain_parts.length - 1]

        init_lock()

        resendMail(pid)
    })

})