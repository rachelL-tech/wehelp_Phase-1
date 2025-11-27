const burger = document.querySelector( '.hamburger');
const drawer = document.querySelector( '.drawer');
const closeBtn = document.querySelector( '.close');

burger.addEventListener('click', () => 
    drawer.classList.add('open')
);
closeBtn.addEventListener('click', () => 
    drawer.classList.remove('open')
);