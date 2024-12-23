document.addEventListener("DOMContentLoaded", () => {
    SOCKET.on('connect', () => {
        log('info', "Socket connected.")
    })

    SOCKET.on('connect_info', (data) => {
        EXEC_MODE = data['exec']
        console.log('info', "Server is running in " + EXEC_MODE + " mode.")
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

    SOCKET.on('reload', () => {
        log('info', "Server requested reload.")
        window.location.reload()
    })

    SOCKET.on('disconnect', () => {
        log('warn', "Socket disconnected... reconnecting.")
    })

    SOCKET.on('error', (error) => {
        log('error', error)
    })
})