document.addEventListener("DOMContentLoaded", function () {
    const username = document.getElementById("user");
    const u_warn = document.getElementById("username_warning");
    const email = document.getElementById("email");
    const e_warn = document.getElementById("email_warning");

    function warn_display(e, type, display) {
        const value = e.target.value

        if (type === 'email' && !value.includes('@'))
            return

        fetch('/availability-check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: value, type: type})
        }).then(res => res.json()).then(data => {
            if (data['available'])
                display.style.display = 'block';
            else
                display.style.display = 'none';
        });
    }

    username.addEventListener("input", function (e) {
        warn_display(e,'username', u_warn);
    });

    email.addEventListener("input", function (e) {
        warn_display(e,'email', e_warn);
    });
});