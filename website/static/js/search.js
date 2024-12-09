function init() {
    const container = document.getElementById("container")
    const search = document.getElementById("search")
    let current = "users"

    function initContainer() {
        if (current === "users") {
            container.querySelectorAll(".list-element").forEach((item) => {
                item.addEventListener("click", (e) => {
                    if (e.target.closest(".relation-btn"))
                        return

                    const username = item.querySelector("#username").textContent
                    window.location.href = `https://growvolution.org/user/${username}`
                })
                item.querySelectorAll(".relation-btn").forEach(btn => {
                    btn.addEventListener("click", (e) => {
                        e.stopPropagation()
                        updateRelation(btn.id, item.querySelector("#username").textContent)
                    })
                })
            })
        }
    }

    function updateRelation(request, user) {
        fetch("/relations", {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: request, receiver: user, breakpoint: true })
        }).then(res => {
            if (res.ok) {
                updateContainer(search.value)
            }
        })
    }

    function updateContainer(request) {
        fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: request, database: current })
        }).then(res => res.text()).then(html => {
            container.innerHTML = html
            initContainer()
        })
    }

    document.querySelectorAll(".headline-row").forEach(row => {
        row.addEventListener("click", () => {
            document.getElementById(current).classList.remove("selected")
            current = row.id
            row.classList.add("selected")
        })
    })

    setInterval(() => {
        if (search.value.length < 1) {
            container.innerHTML = ""
            return
        }

        updateContainer(search.value)
    }, 1000)
}

document.addEventListener("DOMContentLoaded", init);