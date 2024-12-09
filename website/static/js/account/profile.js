function init() {
    const container = document.getElementById("content")
    const share = document.getElementById("share")
    const modal = new bootstrap.Modal(document.getElementById("profile-link"), {})
    const link = document.getElementById("linkText")
    const copied = document.getElementById("copied")

    function initButtons() {
        document.getElementById("nav-container")
        .querySelectorAll(".bi, .relation-btn")
        .forEach((icon) => {
            if (icon.id !== 'share') {
                icon.addEventListener("click", () => {
                    updateContainer(icon.id)
                })
            }
        })

        const new_post = document.querySelector("#new_post")
        if (new_post)
            new_post.addEventListener("click", () => {
                updateContainer("new_post")
            })

        const links = document.getElementById("links")
        links.addEventListener("click", () => {
            updateContainer("links")
        })
    }

    function updateContainer(request, post=null) {
        fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: request, post: post })
        }).then(res => res.text()).then(html => {
            container.innerHTML = html

            container.querySelectorAll("script").forEach(script => {
                eval(script.innerText)
            })

            initButtons()
            initContent()
        })
    }

    function initContent() {
        document.querySelectorAll(".content").forEach(post => {
            post.addEventListener("click", () => {
                updateContainer("post", post.id)
            })
        })
    }

    initButtons()
    initContent()

    if (share)
        share.addEventListener("click", () => {
            modal.show()
        })

    document.getElementById("copyButton").addEventListener("click", () => {
        navigator.clipboard.writeText(link.textContent).then(() => {
            link.style.display = "none"
            copied.style.display = "block"

            setTimeout(() => {
                link.style.display = "block"
                copied.style.display = "none"
            }, 2500)
        })
    })
}

document.addEventListener("DOMContentLoaded", init)