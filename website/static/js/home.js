function init() {
    const container = document.querySelector(".home-container")

    container.style.background = "#cccccc"

    setTab('home')

    function updateContainer(post) {
        fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: 'focus', post: post })
        }).then(res => res.text()).then(html => {
            container.innerHTML = html
            container.style.backgroundColor = "white"

            container.querySelectorAll("script").forEach(script => {
                eval(script.innerText)
            })
        })
    }

    document.querySelectorAll(".post-public").forEach(post => {
        post.addEventListener("click", () => {
            updateContainer(post.id)
        })
    })
}

document.addEventListener("DOMContentLoaded", init)