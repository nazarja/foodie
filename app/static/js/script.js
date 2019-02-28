
function menuAnimation() {
    const logo = document.querySelector('#logo');
    const url = window.location.protocol + '//' + window.location.host + '/';
    let pageOffsetPosition = window.pageYOffset;

    window.addEventListener('scroll', () => {

        if (window.pageYOffset > pageOffsetPosition) {
            logo.style.width = '80px';
            logo.style.height = '60px';
            logo.src = `${url}static/images/logo_small_white.png`;
        }
        else {
            logo.style.width = '120px';
            logo.style.height = '109px';
            logo.src = `${url}static/images/logo_large_white.png`;
        }
        pageOffsetPosition = window.pageYOffset;
    })
}
menuAnimation();