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

    function onRelationUpdate() {
        updateContainer(search.value)
    }
    relationUpdateEventHandler = onRelationUpdate

    function updateRelation(request, user) {
        relationInteraction({
            value: request,
            receiver: user,
            breakpoint: true
        })
    }

    function onSearchResponse(html) {
        container.innerHTML = html
        initContainer()
    }
    searchResponseEventHandler = onSearchResponse

    function updateContainer(request) {
        searchRequest({
            value: request,
            database: current
        })
    }

    document.querySelectorAll(".headline-row").forEach(row => {
        row.addEventListener("click", () => {
            document.getElementById(current).classList.remove("selected")
            current = row.id
            row.classList.add("selected")
        })
    })

   search.addEventListener("input", () => {
       if (search.value.length < 1) {
            container.innerHTML = ""
            return
        }

        updateContainer(search.value)
   })
}

document.addEventListener("DOMContentLoaded", init);