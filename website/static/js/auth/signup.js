document.addEventListener("DOMContentLoaded", function () {
    const username = document.getElementById("user");
    const u_warn = document.getElementById("username_warning");
    const email = document.getElementById("email");
    const e_warn = document.getElementById("email_warning");

    SOCKET.on('availability_response', (data) => {
        if (data.available && data.type === 'email')
            e_warn.style.display = 'block'

        else if (data.available)
            u_warn.style.display = 'block'

        else {
            e_warn.style.display = 'none'
            u_warn.style.display = 'none'
        }
    })

    function warn_display(e, type) {
        const value = e.target.value

        if (type === 'email' && !value.includes('@'))
            return

        SOCKET.emit('availability_check', {
            type: type,
            value: value
        })
    }

    username.addEventListener("input", function (e) {
        warn_display(e,'username', u_warn);
    });

    email.addEventListener("input", function (e) {
        warn_display(e,'email', e_warn);
    });
});