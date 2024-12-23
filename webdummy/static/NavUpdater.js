document.addEventListener("DOMContentLoaded", () => {
    const timer = document.getElementById("day-timer")

    const quotes = [
        '"Zeit ist Geld." ~ <i>Benjamin Franklin</i>',
        '"Wissen ist Macht." ~ <i>Francis Bacon</i>',
        '"Carpe diem." ~ <i>Horaz</i>',
        '"Sei du selbst." ~ <i>Søren Kierkegaard</i>',
        '"Wer wagt, gewinnt." ~ <i>Friedrich Schiller</i>',
        '"Alles fließt." ~ <i>Heraklit</i>',
        '"Lebe und lerne." ~ <i>Unbekannt</i>',
        '"Weniger ist mehr." ~ <i>Ludwig Mies van der Rohe</i>',
        '"Denken ist Leben." ~ <i>Marcus Aurelius</i>',
        '"Tu es einfach." ~ <i>Unbekannt</i>',
        '"Der Weg ist das Ziel." ~ <i>Konfuzius</i>',
        '"Wissen macht frei." ~ <i>Epiktet</i>',
        '"Alles hat seine Zeit." ~ <i>Kohelet</i>',
        '"Kein Risiko, kein Gewinn." ~ <i>Unbekannt</i>',
        '"Nur Mut zählt." ~ <i>Albert Einstein</i>',
        '"Liebe das Leben." ~ <i>Unbekannt</i>',
        '"Nur die Ruhe." ~ <i>Gottfried Keller</i>',
        '"Denken, dann handeln." ~ <i>Unbekannt</i>',
        '"Nur wer fragt, lernt." ~ <i>Unbekannt</i>',
        '"Ordnung ist das halbe Leben." ~ <i>Unbekannt</i>',
        '"Bleib in Bewegung." ~ <i>Aristoteles</i>',
        '"Nichts ist unmöglich." ~ <i>Unbekannt</i>',
        '"Träume groß." ~ <i>Walt Disney</i>',
        '"Einfach machen." ~ <i>Unbekannt</i>',
        '"Lebe jeden Moment." ~ <i>Unbekannt</i>',
        '"Nutze den Tag." ~ <i>Unbekannt</i>',
        '"Glaube an dich." ~ <i>Unbekannt</i>',
        '"Folge deinem Herzen." ~ <i>Unbekannt</i>',
        '"Vertraue dem Prozess." ~ <i>Unbekannt</i>',
        '"Stärke durch Ruhe." ~ <i>Unbekannt</i>'
    ]

    let quoted = false

    function updateTimerText() {
        if (!quoted) {
            const index = Math.floor(Math.random() * quotes.length)
            timer.innerHTML = quotes[index]
            quoted = true
        } else {
            updateTimer()
            quoted = false
        }
    }


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

    setInterval(updateTimerText, 5000)
})