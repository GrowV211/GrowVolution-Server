document.addEventListener("DOMContentLoaded", function () {
    const timeElement = document.getElementById("time");
    let countdown = parseInt(timeElement.textContent);

    const interval = setInterval(function () {
        countdown--;
        timeElement.textContent = countdown.toString();
        if(countdown <= 0) {
            clearInterval(interval);
            window.location.replace("https://growvolution.org/");
        }
    }, 1000);
});