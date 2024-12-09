function init() {
    const container = document.getElementById("listContainer")
    const headline = document.querySelector(".headline-row")

    const elements = document.querySelectorAll(".list-element")

    function updateContainer(request, id=null) {
        fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: request, target: id })
        }).then(res => res.text()).then(html => {
            container.innerHTML = html
            init()
        })
    }

    function initElements() {
        headline.querySelectorAll(".headline-col").forEach(col => {
            col.addEventListener("click", () => {
                if (col.classList.contains("selected"))
                    return

                updateContainer(col.id)
                headline.querySelector(".selected").classList.remove("selected")
                col.classList.add("selected")
            })
        })

        if (elements) {
            elements.forEach(element => {
                element.querySelectorAll("button").forEach(btn => {
                    btn.addEventListener("click", () => {
                        updateContainer(btn.id, element.id)
                    })
                })
            })
        }
    }

    initElements()
}

document.addEventListener("DOMContentLoaded", init)