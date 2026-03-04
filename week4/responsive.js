// let button = document.getElementsByClassName("menu-btn")[0];

// button.addEventListener("click", () => {
//     console.log("Button was clicked!");
// });


const btn = document.querySelector('.menu-btn');
const menu = document.querySelector('nav');

btn.addEventListener('click', toggleMenu);

function toggleMenu() {
    menu.classList.toggle('hide');
    btn.classList.toggle('change');
}