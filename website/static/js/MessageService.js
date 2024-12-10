function updateMessages(data) {
    let type = data.type
    const user = data.user
    if (user) type = `${type} ${user}`

    const element = document.getElementById(type)
    const messages = data.messages

    const requestsText = document.getElementById("requests_text")

    if (messages) {
        element.style.display = "block"

        if (type !== "mod_msgs" && type !== "admin_msgs")
            element.textContent = messages

        if (requestsText && type === "requests")
            requestsText.style.marginLeft = "20px"

        if (user) {
            const last = document.getElementById(user)
            last.style.display = "block"
            last.textContent = data.last
        }
    } else {
        element.style.display = "none"

        if (requestsText && type === "requests")
            requestsText.style.marginLeft = "0"
    }
}