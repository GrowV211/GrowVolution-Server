from website import init_app

HOST = "127.0.0.1"
PORT = 5000

init_app()

if __name__ == '__main__':
    from website import APP, socket
    socket.SOCKET.run(APP, debug=True, host=HOST, port=PORT, allow_unsafe_werkzeug=True)
