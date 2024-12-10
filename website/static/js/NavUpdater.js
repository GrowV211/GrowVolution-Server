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
})