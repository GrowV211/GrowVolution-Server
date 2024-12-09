function init() {
    const container = document.querySelector(".challenge-container")

    container.style.background = "#cccccc"

    function updateContainer(request, post=null) {
        fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: request, post: post })
        }).then(res => res.text()).then(html => {
            container.innerHTML = html
            container.style.backgroundColor = "white"

            container.querySelectorAll("script").forEach(script => {
                eval(script.innerText)
            })
        })
    }

    function updateChallenges(challenge) {
       document.getElementById(challenge).style.display = "none"
    }

    function updateChallenge(command, challenge) {
        fetch(window.location, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({value: command, post: challenge})
        }).then(res => {
            if (res.ok) {
                updateChallenges(challenge)
            }
        })
    }

    function initChallengeButtons() {
        document.querySelectorAll(".challenge-btn").forEach(btn => {
            btn.addEventListener("click", (event) => {
                event.stopPropagation()
                const idParams = btn.id.split(" ")
                updateChallenge(idParams[0], idParams[1])
            })
        })

    }

    document.querySelectorAll(".challenge").forEach(challenge => {
        challenge.addEventListener("click", () => {
            updateContainer("focus", challenge.id)
        })
    })

    initChallengeButtons()
}

document.addEventListener("DOMContentLoaded", init)