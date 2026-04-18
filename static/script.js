function showLogin(){
  document.getElementById("loginForm").classList.remove("hidden");
  document.getElementById("registerForm").classList.add("hidden");

  document.querySelectorAll(".tab")[0].classList.add("active");
  document.querySelectorAll(".tab")[1].classList.remove("active");
}

function showRegister(){
  document.getElementById("loginForm").classList.add("hidden");
  document.getElementById("registerForm").classList.remove("hidden");

  document.querySelectorAll(".tab")[0].classList.remove("active");
  document.querySelectorAll(".tab")[1].classList.add("active");
}

/* show password */
document.addEventListener("click", function(e){
  if(e.target.classList.contains("toggle")){
    let input = e.target.previousElementSibling;
    input.type = input.type === "password" ? "text" : "password";
  }
});
