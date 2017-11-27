/*!
 * @param {number} duration - The speed amount
 * @param {string} easing - The easing method
 * @param {function} complete - A callback function
**/
jQuery.fn.blindLeftToggle = function (duration, easing, complete) {
    return this.animate({
        marginLeft: parseFloat(this.css('marginLeft')) < 0 ? 0 : -this.outerWidth()
    }, jQuery.speed(duration, easing, complete));
};

/*!
 * @param {number} duration - The speed amount
 * @param {string} easing - The easing method
 * @param {function} complete - A callback function
**/
jQuery.fn.blindLeftOut = function (duration, easing, complete) {
    return this.animate({
        marginLeft: -$('.left-panel').width()-10
    }, jQuery.speed(duration, easing, complete));
};

/*!
 * @param {number} duration - The speed amount
 * @param {string} easing - The easing method
 * @param {function} complete - A callback function
**/
jQuery.fn.blindLeftIn = function (duration, easing, complete) {
    return this.animate({
        marginLeft: 0
    }, jQuery.speed(duration, easing, complete));
};

$('.navbar-map').click(function(e) {
    e.preventDefault();
    // Important for mobile
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
    $('.left-panel').addClass('mobile-hide');
    $('.right-panel').removeClass('mobile-hide');
});

$('.navbar-gallery').click(function(e) {
    e.preventDefault();
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    showGalleryTab();
});

$('.navbar-getinvolved').click(function(e) {
    e.preventDefault();
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    collapseCard();
    collapseMap();
    history.replaceState({}, null, '/');
    showGetInvolvedTab();
});

$('.navbar-whatsnew').click(function(e) {
    e.preventDefault();
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    collapseCard();
    collapseMap();
    history.replaceState({}, null, '/');
    showWhatsNewTab();
});


/* Set the width of the side navigation to 250px and the left margin of the page content to 250px and add a black background color to body */
function openNav() {
    $('#mySidenav').css('width', '90%');
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
function closeNav() {
    $('#mySidenav').css('width', '0');
}

$('.navbar-item').hover(function () {
    $(this).find('.navbar-dropdown').css('display', 'block');
}, function () {
    $(this).find('.navbar-dropdown').css('display', 'none');
});

