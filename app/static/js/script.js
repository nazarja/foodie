
function menuAnimation() {
    const logo = document.querySelector('#logo');
    const url = window.location.protocol + '//' + window.location.host + '/';
    let pageOffsetPosition = window.pageYOffset;

    window.addEventListener('scroll', () => {

        if (window.pageYOffset > pageOffsetPosition) {
            logo.style.width = '80px';
            logo.style.height = '60px';
            logo.src = `${url}static/images/logo_small_white.png`;
            changeDropDown('0');
        }
        else {
            logo.style.width = '120px';
            logo.style.height = '109px';
            logo.src = `${url}static/images/logo_large_white.png`;
            changeDropDown('15');
        }
        pageOffsetPosition = window.pageYOffset;
    })
}
menuAnimation();



function changeDropDown(offset) {    
    const menus = document.querySelectorAll('.main-dropdown-menu');
    menus.forEach(menu => menu.setAttribute('uk-drop', `offset: ${offset}`));
};
