let SOCKET

function connectSocket() {
    return io('https://growvolution.org', {
      reconnection: true,          // Aktiviert die automatische Wiederverbindung
      reconnectionAttempts: 5,     // Anzahl der Versuche
      reconnectionDelay: 1000,     // Wartezeit vor dem ersten Versuch (in ms)
      reconnectionDelayMax: 5000,  // Maximale Wartezeit zwischen den Versuchen (in ms)
      timeout: 20000               // Verbindungs-Timeout (in ms)
    })
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

    SOCKET.on('update_messages', (data) => {
        let type = data.type
        const user = data.user
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
                last.style.display = "block"
                last.textContent = data.last
            }
        } else {
            element.style.display = "none"

            if (requestsText && type === "requests")
                requestsText.style.marginLeft = "0"
        }
    })

    SOCKET.on('disconnect', () => {
        console.warn("Socket disconnected... reconnecting.")
    })
})