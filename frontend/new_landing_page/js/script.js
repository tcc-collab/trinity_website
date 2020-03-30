
// navigation
document.querySelector('.nav_btn').addEventListener('click',navReveal);
document.querySelector('.dark_body').addEventListener('click',navReveal);

var className = document.getElementsByClassName('nav_btn')[0].classList;


document.addEventListener('keydown',function(event){
    if((event.keyCode === 27 || event.which === 27) && className[1] === 'clicked_btn'){
       navReveal();
    }
});

function navReveal(){
    document.querySelector('.primary_nav').classList.toggle('primary_nav_reveal');

    document.querySelector('.nav_btn').classList.toggle('clicked_btn');
    document.querySelector('.nav_icon_2').classList.toggle('clicked_icon_2');
    document.querySelector('.nav_icon_1').classList.toggle('clicked_icon_1');
    document.querySelector('.nav_icon_3').classList.toggle('clicked_icon_3');
    document.querySelector('.dark_body').classList.toggle('clicked_dark_body');

}




// dropdown

var dropdown = document.querySelectorAll('.dropdown_btn');

var arrDropdown = Array.prototype.slice.call(dropdown);

arrDropdown.forEach( addIcon);
function addIcon(current,i,arr){
    current.insertAdjacentHTML('afterbegin','<i class="fas fa-angle-down drop_icon"></i>');

}

arrDropdown.forEach(function(current,i,arr){
    current.addEventListener('click', function(){
        this.nextElementSibling.classList.toggle('clicked_dropdown');
        this.firstChild.classList.toggle('active_drop');
    });
});
