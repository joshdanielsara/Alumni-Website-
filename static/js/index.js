const loginsec=document.querySelector('.login-section')
const loginlink=document.querySelector('.login-link')
const registerlink=document.querySelector('.register-link')
registerlink.addEventListener('click',()=>{
    loginsec.classList.add('active')
})
loginlink.addEventListener('click',()=>{
    loginsec.classList.remove('active')
})




const togglePasswordVisibility = (passwordFieldId, toggleButtonId) => {
    const passwordInput = document.getElementById(passwordFieldId);
    const toggleButton = document.getElementById(toggleButtonId);

    toggleButton.addEventListener("click", function() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    });
};

// Add event listeners to both password fields
togglePasswordVisibility("password1", "togglePassword1");
togglePasswordVisibility("password2", "togglePassword2");
