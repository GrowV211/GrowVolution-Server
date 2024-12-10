function init() {
    const container = document.querySelector(".chats-container")
    const chats = document.querySelectorAll(".list-element")

    setTab('chats')

    function onUpdate(data) {
        let html
        let type

        if (typeof data === 'string') {
            html = data
            type = 'chat'
        } else {
            html = data.html
            type = data.type
        }

        container.innerHTML = html

        if (type === 'chats')
            init()

        else
            container.querySelectorAll("script").forEach(script => {
                eval(script.innerText)
            })
    }

    updateEventHandler = onUpdate

    chats.forEach(chat => {
        chat.addEventListener("click", () => {
            const username = chat.querySelector("#username").textContent.trim()
            joinChat(username)
        })
    })
}

document.addEventListener("DOMContentLoaded", init)