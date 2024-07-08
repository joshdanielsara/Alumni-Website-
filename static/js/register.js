document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode');
    const container = document.querySelector(".container");

    // Default to sign-up mode if no mode parameter is provided or if mode is 'sign-up'
    if (mode === 'sign-in') {
        container.classList.remove("sign-up-mode");
    } else {
        container.classList.add("sign-up-mode");
    }

    const sign_in_btn = document.querySelector("#sign-in-btn");
    const sign_up_btn = document.querySelector("#sign-up-btn");

    if (sign_up_btn) {
        sign_up_btn.addEventListener("click", () => {
            container.classList.add("sign-up-mode");
        });
    }

    if (sign_in_btn) {
        sign_in_btn.addEventListener("click", () => {
            container.classList.remove("sign-up-mode");
        });
    }
});
