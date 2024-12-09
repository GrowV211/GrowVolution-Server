function init() {
    const container = document.querySelector(".chats-container")
    const chats = document.querySelectorAll(".list-element")

    SOCKET.emit('set_tab', 'chats')

    SOCKET.on("update", (data) => {
        container.innerHTML = data.html

        if (data.type === 'chats')
            init()

        else
            container.querySelectorAll("script").forEach(script => {
                eval(script.innerText)
            })
    })

    chats.forEach(chat => {
        chat.addEventListener("click", () => {
            const username = chat.querySelector("#username").textContent.trim()
            SOCKET.emit("open_chatroom", {
                username: username,
                destination: 'chats'
            })
        })
    })
}

document.addEventListener("DOMContentLoaded", init)