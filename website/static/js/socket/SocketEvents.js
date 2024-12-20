function clearSession() {
    sessionStorage.removeItem('password')
    sessionStorage.removeItem('username')
}

document.addEventListener("DOMContentLoaded", () => {
    SOCKET.on('connect', () => {
        log('info', "Socket connected.")
    })

    SOCKET.on('connect_info', (data) => {
        EXEC_MODE = data['exec']
        if (data['has_user'] && !sessionStorage.getItem('username')) {
            if (localStorage.getItem('user_key'))
                localStorage.removeItem('user_key')
            else
                window.location.href = "https://growvolution.org/logout"
        } else if (!data['has_user'] && sessionStorage.getItem('username')) {
            clearSession()
        }
    })

    SOCKET.on('user_salt', (salt) => {
        console.log('dbg:', salt)
        generateKey([
            sessionStorage.getItem('username'),
            sessionStorage.getItem('password')
        ], salt)
            .then(key => exportKeyToString(key))
            .then(keyString => {
                localStorage.setItem('user_key', keyString)
                clearSession()
            })
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
        log('warn', "Socket disconnected... reconnecting.")
    })

    SOCKET.on('error', (error) => {
        log('error', error)
    })
})