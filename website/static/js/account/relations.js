function init() {
    const container = document.getElementById('container');
    let current = "active"

    function initContainer() {
        container.querySelectorAll(".list-element").forEach(item => {
            item.addEventListener("click", (e) => {
                if(e.target.closest(".relation-btn"))
                    return

                const username = item.querySelector("#username").textContent
                window.location.href = `https://growvolution.org/user/${username}`
            });
            item.querySelectorAll(".relation-btn").forEach(btn => {
                btn.addEventListener("click", (e) => {
                    e.stopPropagation()
                    updateContainer(btn.id, item.querySelector("#username").textContent)
                })
            })
        })
    }

    function onRelationUpdate(html) {
        container.innerHTML = html
        initContainer()
    }
    relationUpdateEventHandler = onRelationUpdate

    function updateContainer(request, user=null) {
        relationInteraction({
            value: request,
            container: current,
            receiver: user
        })
    }

    document.querySelectorAll(".headline-row").forEach(row => {
        row.addEventListener("click", (e) => {
            document.getElementById(current).classList.remove("selected")
            current = row.id
            row.classList.add("selected")
            updateContainer(current)
        })
    })

    initContainer()
}

document.addEventListener("DOMContentLoaded", init)