document.addEventListener("DOMContentLoaded", () => {
    const entries = document.getElementById("entries")
    const journal = document.getElementById("journal")
    const journalForm = document.getElementById("journal_form")

    if (journal)
        journal.addEventListener("submit", (event) => {
            event.preventDefault()

            const form = event.target

            if (!form.checkValidity()) {
                form.reportValidity()
                return
            }

            event.target.reset()

            const formData = new FormData(form)

            fetch(window.location, {
                method: "POST",
                body: formData
            }).then(res =>  res.text()).then(html => {
                entries.innerHTML = html

                journalForm.style.display = "none"
            })
        })
})