document.addEventListener("DOMContentLoaded", () => {
    SOCKET.on('connect', (exec_mode) => {
        EXEC_MODE = exec_mode
        log('info', "Socket connected.")
    })

    SOCKET.on('update_messages', updateMessages)

    SOCKET.on('update', (data) => {
        updateEventHandler(data)
    })

    SOCKET.on('profile_update', (data) => {
        profileEditEventHandler(data)
    })

    SOCKET.on('search_response', (html) => {
        searchResponseEventHandler(html)
    })

    SOCKET.on('edit_reset', (data) => {
        editResetEventHandler(data)
    })

    SOCKET.on('pp_delete', (html) => {
        deletePPEventHandler(html)
    })

    SOCKET.on('relation_update', (data) => {
        relationUpdateEventHandler(data)
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
        log('warning', "Socket disconnected... reconnecting.")
    })
})