document.addEventListener("DOMContentLoaded", () => {
    SOCKET.on('connect', () => {
        console.log("Socket connected: ", SOCKET.connected)
    })

    SOCKET.on('update_messages', updateMessages)

    SOCKET.on('update', (data) => {
        updateEventHandler(data)
    })

    SOCKET.on('profile_update', (data) => {
        profileEditEventHandler(data)
    })

    SOCKET.on('edit_reset', (data) => {
        editResetEventHandler(data)
    })

    SOCKET.on('pp_delete', (html) => {
        deletePPEventHandler(html)
    })

    SOCKET.on('update_chat', (data) => {
        chatMessageEventHandler(data)
    })

    SOCKET.on('resend_info', (lockTime) => {
        resendInfoEventHandler(lockTime)
    })

    SOCKET.on('availability_response', (data) => {
        availabilityResponseHandler(data)
    })

    SOCKET.on('disconnect', () => {
        console.warn("Socket disconnected... reconnecting.")
    })
})