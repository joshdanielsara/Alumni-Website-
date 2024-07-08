document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode');
    const container = document.querySelector(".container");
  
    // Initially remove the class to trigger the animation later
    container.classList.remove("sign-up-mode");
  
    // Use setTimeout to delay adding the class to trigger the animation
    setTimeout(() => {
      if (mode === 'sign-up') {
        container.classList.add("sign-up-mode");
      } else {
        container.classList.remove("sign-up-mode");
      }
    }, 10); // Delay in milliseconds (adjust if necessary)
  
    const sign_in_btn = document.querySelector("#sign-in-btn");
    const sign_up_btn = document.querySelector("#sign-up-btn");
  
    sign_up_btn.addEventListener("click", () => {
      container.classList.add("sign-up-mode");
    });
  
    sign_in_btn.addEventListener("click", () => {
      container.classList.remove("sign-up-mode");
    });
  });
  