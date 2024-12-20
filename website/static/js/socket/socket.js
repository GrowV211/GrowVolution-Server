function connectSocket() {
    return io('wss://growvolution.org', {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 20000
    })
}

const SOCKET = connectSocket()
