
/*
==================================================================
    Menu Animation
==================================================================
*/

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
        };
        pageOffsetPosition = window.pageYOffset;
    });
};
menuAnimation();



function changeDropDown(offset) {    
    const menus = document.querySelectorAll('.main-dropdown-menu');
    menus.forEach(menu => menu.setAttribute('uk-drop', `offset: ${offset}`));
}


/*
==================================================================
    XMLHTTPRequest fort Comments
==================================================================
*/

function listenForComments() {

    if (document.querySelector('#recipe')) {

        const form = document.querySelector('#comments-form');
        const userComments = document.querySelector('#user-comments');
        const placeholder = document.querySelector('#comments-placeholder');
        const data = document.querySelector('#hidden-input');
        const reply = document.querySelector('#form-reply-comment');
        

        form.addEventListener('submit', (event) => {
            event.preventDefault()
            const date = new Date().toLocaleString();
            

            let xhr = new XMLHttpRequest();
            xhr.open("POST", '/comments', true);
            xhr.onreadystatechange = function(res) { 
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {

                    const comment =
                    `<article class="uk-comment uk-padding-small uk-margin-medium">
                    <header class="uk-comment-header uk-grid-medium uk-flex-middle" uk-grid>
                    <div class="uk-width-auto">
                    <img class="uk-comment-avatar" src="../../static/images/profile_picture.png" width="80" height="80" alt="profile picture"></div>
                    <div class="uk-width-expand"><h4 class="uk-comment-title uk-margin-remove">${data.value}</h4>
                    <ul class="uk-comment-meta uk-subnav uk-subnav-divider uk-margin-remove-top"><li>${date}</li>
                    </ul></div></header><div class="uk-comment-body">
                    <p class="comment">${reply.value}</p></div></article>`;
                                
                    if (placeholder) placeholder.style.display = 'none';
                    userComments.insertAdjacentHTML("beforeend", comment);
                    reply.value = '';
                };
            };
            xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
            xhr.send(`recipe_id=${recipe_id}&username=${data.value}&date=${date}&reply=${reply.value}`); 
        });
    };
};
listenForComments();
