let selectElem = document.querySelector('select');
let logo = document.querySelector('img');
let pageContent = document.querySelector('body');

let intro = document.querySelector('#intro');

selectElem.addEventListener('change', changeTheme);

function changeTheme() {
    let current = selectElem.value;
    if (current == 'dark') {
        // code for changes to colors and logo
        pageContent.style.backgroundColor = '#1e1e1e';
        pageContent.style.color = 'white';
        intro.style.color = 'white';
        logo.src = 'dark-byui.png';
        logo.style.filter = 'none';
    } else {
        // code for changes to colors and logo
        pageContent.style.backgroundColor = 'white';
        pageContent.style.color = 'black';
        intro.style.color = 'black';
        logo.src = 'byui-logo-blue.webp';
        logo.style.filter = 'none';
    }
}           
                    