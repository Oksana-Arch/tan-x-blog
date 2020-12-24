function myFunction() {
    alert('You comment has been added');
}
$('.collapse-btn').on('click', function (e) {
    e.preventDefault();
    $('.collapse-menu').toggleClass('collapse-menu-active');
    $('.collapse-btn').toggleClass('collapse-btn-active');
    $('.btn-group').toggleClass('btn-group-active');
})

$(document).ready(function () {
    var button = $('#back_to_top');
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            button.fadeIn();
        } else {
            button.fadeOut();
        }
    });
    button.on('click', function () {
        $('body, html').animate({
            scrollTop: 0
        }, 1000);
        return false;
    });
});