function init() {
    const container = document.querySelector(".challenge-container")
    const modal = new bootstrap.Modal(document.getElementById('uploadEvidenceModal'));

    const submitEvidenceButton = document.getElementById("submitEvidence");
    const submitWithoutEvidenceButton = document.getElementById("submitWithoutEvidence");
    const evidenceForm = document.getElementById("evidenceForm");

    let challengeID

    submitEvidenceButton.addEventListener("click", () => {
        const formData = new FormData(evidenceForm);
        const files = formData.getAll("files");

        if (files.length > 5) {
          alert("Du kannst maximal 5 Dateien hochladen.");
          return;
        } else if(files.length < 1) {
            alert("Du musst mindestens eine Datei hochladen oder ohne Beweis fortfahren.")
            return
        }

        sendFormData(formData);
    });

    submitWithoutEvidenceButton.addEventListener("click", sendFormNoEvidence);

    function sendFormNoEvidence() {
        const formData = new FormData();
        formData.append("no_evidence", true);

        sendFormData(formData);
    }

    function sendFormData(formData) {
        formData.append("challenge", challengeID)

        fetch(window.location, {
        method: "POST",
        body: formData,
        }).then(res => {
          if (res.ok) {
              modal.hide()

              const challenge = document.getElementById(challengeID)

              const finishButton = challenge.querySelector("#finish")
              finishButton.textContent = "Erledigt"
              finishButton.classList.remove("btn-primary")
              finishButton.classList.add("btn-secondary")
              finishButton.disabled = true

              const cancelButton = challenge.querySelector("#cancel")
              cancelButton.disabled = true
          }
        })
    }

    function updateContainer(request, challenge) {
        fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: request, post: challenge })
        }).then(res => res.text()).then(html => {
            container.innerHTML = html
            init()
        })
    }

    document.querySelectorAll(".challenge").forEach(challenge => {
        challenge.querySelectorAll("button").forEach(btn => {
            if (btn.id && !btn.disabled) {
                btn.addEventListener("click", () => {
                    if (btn.id === "finish") {
                        challengeID = challenge.id

                        if (challenge.classList.contains("provable")) {
                            modal.show()
                        } else {
                            sendFormNoEvidence()
                        }
                    }
                    else {
                        updateContainer(btn.id, challenge.id)
                    }
                })
            }
        })
    })
}

document.addEventListener("DOMContentLoaded", init)