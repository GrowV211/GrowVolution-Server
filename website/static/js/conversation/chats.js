function init() {
    const container = document.querySelector(".chats-container")
    const chats = document.querySelectorAll(".list-element")

    SOCKET.on("update_container", (html) => {
        container.innerHTML = html

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