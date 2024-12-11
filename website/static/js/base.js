let EXEC_MODE

function log(category, message) {
    if (EXEC_MODE === 'DEBUG') {
        console.log(`[${getTime()}] [${category.toUpperCase()}] ${message}`)
    }
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

function getTime() {
    const date = new Date()

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`
}

document.addEventListener("DOMContentLoaded", () => {
    if (!localStorage['license-shown']) {
        flash("<b>Hinweis:</b> Der gesamte Quellcode dieser Seite ist unter einer <i>GNU General Public License</i> freigegeben. " +
            "Ihre Ausgangsversion läuft auf <a href='https://growvolution.org'>growvolution.org</a>.", 'warning')
        localStorage['license-shown'] = true
    }
})