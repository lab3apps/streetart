/* View States:
 * 0: Default large left panel with gallery.
 * 1: Large map panel with small card and gallery.
 * 2: Large left panel with expanded Card.
 */
var viewState = 0;


function markerClicked() {
    if(viewState === 0 || viewState === 1) {
        expandMap();
    }
    // Hide image while other loads. This will break linking.
    //$('.main-image').attr('src', '');
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    showLeftPanel();
}

function backClicked() {
    gallery_view();
   
    history.replaceState({}, null, '/');
    return;
    if(viewState === 1){
        collapseMap();
    } else if (viewState === 2) {
        collapseCard();
    }
}
/*
function focusRight() {
    $('.left-panel').removeClass('col-md-7');
    $('.left-panel').addClass('col-md-4');
    $('.right-panel').removeClass('col-md-5');
    $('.right-panel').addClass('col-md-8');
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 100);
}

function focusLeft() {
    $('.left-panel').removeClass('col-md-4');
    $('.left-panel').addClass('col-md-7');
    $('.right-panel').removeClass('col-md-8');
    $('.right-panel').addClass('col-md-5');
    
        google.maps.event.trigger(map, "resize");
    
}*/

function gallery_view() {
    $('#comment-card-holder').hide();
    $('#images-card-holder').hide();
    $('.scroll-gallery').show();
    $('.left-panel').css('overflow-y', 'hidden');
    $('.main-image').css('height', '30%');
    $(".card-details").slideUp();
    $(".overlay").fadeIn();

    $('#marker-card-holder').hide();
    $('.title-block').show();
    $('.back-block').hide();
    $('.gallery-item').removeClass('col-md-6');
    $('.gallery-item').addClass('col-md-3');
    // Important for mobile
    $('.left-panel').addClass('mobile-hide');
    $('.right-panel').removeClass('mobile-hide');

    viewState = 0;
}

function full_map_view() {

}

function full_card_view() {
    $('#marker-card-holder').show();
    $('.title-block').hide();
    $('.back-block').show();
    $('.gallery-item').removeClass('col-md-3');
    $('.gallery-item').addClass('col-md-6');
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');

    $('#comment-card-holder').show();
    $('#images-card-holder').show();
    $('.scroll-gallery').hide();
    $('.left-panel').css('overflow-y', 'scroll');
    $('.main-image').css('height', '25%');
    $(".card-details").slideDown();
    $(".overlay").fadeOut();
    viewState = 2;

    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    showLeftPanel();
}

function expandMap() {
    //focusRight();
    $('#marker-card-holder').show();
    $('.title-block').hide();
    $('.back-block').show();
    $('.gallery-item').removeClass('col-md-3');
    $('.gallery-item').addClass('col-md-6');
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    viewState = 1;
}

function collapseMap() {
    //focusLeft();
    $('#marker-card-holder').hide();
    $('.title-block').show();
    $('.back-block').hide();
    $('.gallery-item').removeClass('col-md-6');
    $('.gallery-item').addClass('col-md-3');
    // Important for mobile
    $('.left-panel').addClass('mobile-hide');
    $('.right-panel').removeClass('mobile-hide');

    viewState = 0;
}


function expandCard() {
    //focusLeft();
    $('#comment-card-holder').show();
    $('#images-card-holder').show();
    $('.scroll-gallery').hide();
    $('.left-panel').css('overflow-y', 'scroll');
    $('.main-image').css('height', '25%');
    $(".card-details").slideDown();
    $(".overlay").fadeOut();
    viewState = 2;
}

function collapseCard() {
    //focusRight();
    $('#comment-card-holder').hide();
    $('#images-card-holder').hide();
    $('.scroll-gallery').show();
    $('.left-panel').css('overflow-y', 'hidden');
    $('.main-image').css('height', '30%');
    $(".card-details").slideUp();
    $(".overlay").fadeIn();
    viewState = 1;
}

function hideLeftPanel() {
    $('.left-panel').addClass('no-width');
    $('.right-panel').addClass('full-width');
    $('.right-panel-toggle').hide();
    $('.left-panel-toggle').removeClass('material-icons');
    $('.left-panel-toggle').text('SHOW GALLERY');
}

function showLeftPanel() {
    $('.left-panel').removeClass('no-width');
    $('.right-panel').removeClass('full-width');
    $('.right-panel-toggle').show();
    $('.left-panel-toggle').addClass('material-icons');
    $('.left-panel-toggle').text('arrow_upward');
}
function hideRightPanel() {
    $('.right-panel').addClass('no-width');
    $('.left-panel').addClass('full-width-minus-buttons');
    $('.left-panel-toggle').hide();
    $('.right-panel-toggle').removeClass('material-icons');
    $('.right-panel-toggle').text('SHOW MAP');
}

function showRightPanel() {
    $('.right-panel').removeClass('no-width');
    $('.left-panel').removeClass('full-width-minus-buttons');
    $('.left-panel-toggle').show();
    $('.right-panel-toggle').addClass('material-icons');
    $('.right-panel-toggle').text('arrow_downward');
}

function resizeMap() {
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
}

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

});

$('#left-panel-toggle').click(function(e) {
    if ($('.left-panel').hasClass('no-width')) {
        showLeftPanel();
    } else {
        hideLeftPanel();
    }
    resizeMap();
});

$('#right-panel-toggle').click(function(e) {
    if ($('.right-panel').hasClass('no-width')) {
        showRightPanel();
    } else {
        hideRightPanel();
    }
    resizeMap();
});

function activateSnackbar(snackbarDiv) {
    $(snackbarDiv).addClass('show');
    setTimeout(function() {
        $(snackbarDiv).removeClass('show');
    }, 3000);
}

