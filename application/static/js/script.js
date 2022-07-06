let hamb = document.querySelector(".hamb");
let menu = document.querySelector(".menu");

hamb.addEventListener("click", mobileMenu);

function mobileMenu(){
    hamb.classList.toggle("active");
    menu.classList.toggle("active");
}

const link = document.querySelectorAll(".link");
link.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu(){
    hamb.classList.remove("active");
    menu.classList.remove("active");
}