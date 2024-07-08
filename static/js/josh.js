



















const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("togglePassword");

toggleButton.addEventListener("click", function() {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";

  } else {
    passwordInput.type = "password";
  
  }
});

const passwordInpu = document.getElementById("confirmPassword");
const toggleButto = document.getElementById("togglePassword");

toggleButto.addEventListener("click", function() {
  if (passwordInpu.type === "password") {
    passwordInpu.type = "text";

  } else {
    passwordInpu.type = "password";
  
  }
});

const passwordInp = document.getElementById("pass");
const toggleButt = document.getElementById("toggle");

toggleButt.addEventListener("click", function() {
  if (passwordInp.type === "password") {
    passwordInp.type = "text";

  } else {
    passwordInp.type = "password";
  
  }
});


