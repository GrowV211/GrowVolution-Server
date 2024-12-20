function setTab(tab) {
    SOCKET.emit('set_tab', tab)
}

function back() {
    SOCKET.emit('back')
}

function searchRequest(data) {
    SOCKET.emit('search', data)
}

function forgotQuery(data) {
    SOCKET.emit('forgot_query', data)
}

function resendMail(pid) {
    SOCKET.emit('resend_mail', pid)
}

function profileInteraction(data) {
    SOCKET.emit('profile_interaction', data)
}

function availabilityCheck(data) {
    SOCKET.emit('availability_check', data)
}

function editProfile(data) {
    SOCKET.emit('edit_profile', data)
}


function resetEdit() {
    SOCKET.emit('reset_edit')
}

function deletePP() {
    SOCKET.emit('delete_pp')
}

function relationInteraction(data) {
    SOCKET.emit('relation_interaction', data)
}

function joinChat(name) {
    SOCKET.emit('join_chatroom', name)
}

function sendChatMessage(data) {
    SOCKET.emit('chat_message', data)
}

function contentInteraction(data) {
    SOCKET.emit('content_interaction', data)
}