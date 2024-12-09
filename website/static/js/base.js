let SOCKET

function connectSocket() {
    return io.connect('https://growvolution.org')
}

function flash(message, category) {
    const flashContainer = document.getElementById("flashContainer")

    flashContainer.innerHTML = `
        <div class="alert alert-${category} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `
}

document.addEventListener("DOMContentLoaded", () => {
    const timer = document.getElementById("day-timer")

    function getMinutesRemaining() {
        const now = new Date()
        const totalMinutesADay = 1440
        const minutesPassedToday = now.getHours() * 60 + now.getMinutes()
        return totalMinutesADay - minutesPassedToday
    }

    function updateTimer() {
        const minutesRemaining = getMinutesRemaining()
        timer.textContent = `${minutesRemaining} Minuten vom Tag übrig.`
    }

    updateTimer()

    setInterval(updateTimer, 60000)

    SOCKET = connectSocket()

    SOCKET.on('no_user', SOCKET.disconnect)

    SOCKET.on('update_messages', (data) => {
        let type = data.msgType
        const user = data.usr
        if (user) type = `${type} ${user}`

        const element = document.getElementById(type)
        const messages = data.messages

        const requestsText = document.getElementById("requests_text")

        if (messages) {
            element.style.display = "block"

            if (type !== "mod_msgs" && type !== "admin_msgs")
                element.textContent = messages

            if (requestsText && type === "requests")
                requestsText.style.marginLeft = "20px"

            if (user) {
                const last = document.getElementById(user)
                const last_msg = data.lastMsg
                if (last_msg) {
                    last.style.display = "block"
                    last.textContent = last_msg
                } else {
                    last.style.display = "none"
                }
            }
        } else {
            element.style.display = "none"

            if (requestsText && type === "requests")
                requestsText.style.marginLeft = "0"
        }
    })

    SOCKET.on('disconnect', () => {
        SOCKET.disconnect()

        setTimeout(() => {
            SOCKET = connectSocket()
        }, 2500)
    })
})