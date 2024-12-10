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
    if (!localStorage['license-shown']) {
        flash("<b>Hinweis:</b> Der gesamte Quellcode dieser Seite ist unter einer <i>GNU General Public License</i> freigegeben. " +
            "Ihre Ausgangsversion läuft auf <a href='https://growvolution.org'>growvolution.org</a>.", 'warning')
        localStorage['license-shown'] = true
    }
})