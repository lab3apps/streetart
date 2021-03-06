function markerClicked() {
    
    // Hide image while other loads. This will break linking.
    //$('.main-image').attr('src', '');
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    $('.gallery-menu-items').hide();
    showLeftPanel();
}

function backClicked() {
    gallery_view();
   
    history.replaceState({}, null, '/');
}

function gallery_view() {
    $('#comment-card-holder').hide();
    $('#images-card-holder').hide();
    $('#nearest-artworks-holder').hide();
    $('#nearest-artworks-header').hide();
    $('.scroll-gallery').show();
    $('.left-panel').css('overflow-y', 'hidden');
    $(".card-details").slideUp();
    $(".overlay").fadeIn();

    $('#marker-card-holder').hide();
    $('.title-block').show();
    $('.back-block').hide();
    // Important for mobile
    $('.right-panel').addClass('mobile-hide');
    $('.left-panel').removeClass('mobile-hide');
}

function full_card_view() {
    var elem = document.querySelector(".card .card-image img");

    //Get inital size. Animating map (right-panel)
    var collapsed = elem.getBoundingClientRect();

    elem.classList.add('expanding-img');

    $('.gallery-menu-items').hide();
    $('#marker-card-holder').show();
    $('.title-block').hide();
    $('.back-block').show();
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');

    $('#comment-card-holder').show();
    $('#images-card-holder').show();
    $('#nearest-artworks-holder').show();
    $('#nearest-artworks-header').show();
    $('.scroll-gallery').hide();
    $('.left-panel').css('overflow-y', 'scroll');
    $(".card-details").slideDown();
    $(".overlay").fadeOut();
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    showLeftPanel();

    var expanded = elem.getBoundingClientRect();

    //Invert
    var invertedTop = collapsed.top - expanded.top;
    var invertedLeft = collapsed.left - expanded.left;
    // Use divisions when manipulating sizes to apply in scale
    var invertedWidth = collapsed.width / expanded.width;
    var invertedHeight = collapsed.height / expanded.height;

    elem.style.transformOrigin = 'center';

    elem.style.transform = 'translate(' + invertedLeft + 'px, ' + invertedTop + 'px) scale(' + invertedWidth + ', ' + invertedHeight + ')';

    requestAnimationFrame(function(){
        // Add the class to run the transition
        elem.classList.add('transition-img'); 
        // Clear styles
        elem.style.transform = '';
        // On transitionEnd remove the classes used control transitions
        elem.addEventListener('transitionend', function(){
            elem.style.transformOrigin = '';
            elem.classList.remove('transition-img');
            elem.classList.remove('expanding-img');
            // Remove the eventListener
            elem.removeEventListener('transitionend', this, false);
        });
    }); 
}

function hideLeftPanel() {
    $('.left-panel').addClass('no-width');
    $('.right-panel').addClass('full-width');
    $('.right-panel-toggle').hide();
    $('.left-panel-toggle').removeClass('material-icons');
    $('.left-panel-toggle').text('SHOW GALLERY');
    $('.back-block').hide();
}

function showLeftPanel() {
    $('.left-panel').removeClass('no-width');
    $('.right-panel').removeClass('full-width');
    $('.right-panel-toggle').show();
    $('.left-panel-toggle').addClass('material-icons');
    $('.left-panel-toggle').text('arrow_drop_up');
    if ($('.scroll-gallery').css('display') == 'none') {
        $('.back-block').show();
    }
}
function hideRightPanel() {
    $('.right-panel').addClass('no-width');
    $('.left-panel').addClass('full-width-minus-buttons');
    $('.left-panel-toggle').hide();
    $('.right-panel-toggle').removeClass('material-icons');
    $('.right-panel-toggle').text('SHOW MAP');
    $('.gallery-item').removeClass('col-lg-6');
    $('.gallery-item').removeClass('col-sm-6');
    $('.gallery-item').addClass('col-sm-4');
    $('.gallery-item').addClass('col-lg-3');
    $('.gallery-item').addClass('col-xl-2');
    $('.right-panel-toggle').css("top","40%");
}

function showRightPanel() {
    $('.right-panel').removeClass('no-width');
    $('.left-panel').removeClass('full-width-minus-buttons');
    $('.left-panel-toggle').show();
    $('.right-panel-toggle').addClass('material-icons');
    $('.right-panel-toggle').text('arrow_drop_down');
    $('.gallery-item').addClass('col-lg-6');
    $('.gallery-item').addClass('col-sm-6');
    $('.gallery-item').removeClass('col-sm-4');
    $('.gallery-item').removeClass('col-lg-3');
    $('.gallery-item').removeClass('col-xl-2');
    $('.right-panel-toggle').css("top", "calc(40% + 80px)");
}

function resizeMap() {
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 200);
}

function perform_left_toggle() {
    var elem = document.querySelector(".right-panel");

    //Get inital size. Animating map (right-panel)
    var collapsed = elem.getBoundingClientRect();

    elem.classList.add('expanding');

    if ($('.left-panel').hasClass('no-width')) {
        showLeftPanel();
    } else {
        hideLeftPanel();
    }
    

    var expanded = elem.getBoundingClientRect();

    //Invert
    var invertedTop = collapsed.top - expanded.top;
    var invertedLeft = collapsed.left - expanded.left;
    // Use divisions when manipulating sizes to apply in scale
    var invertedWidth = collapsed.width / expanded.width;
    var invertedHeight = collapsed.height / expanded.height;

    elem.style.transformOrigin = 'top left';

    elem.style.transform = 'translate(' + invertedLeft + 'px, ' + invertedTop + 'px) scale(' + invertedWidth + ', ' + invertedHeight + ')';

    requestAnimationFrame(function(){
        // Add the class to run the transition
        elem.classList.add('transition'); 
        // Clear styles
        elem.style.transform = '';
        // On transitionEnd remove the classes used control transitions
        elem.addEventListener('transitionend', function(){
            elem.style.transformOrigin = '';
            elem.classList.remove('transition');
            elem.classList.remove('expanding');
            //trigger map resize on animation complete
            google.maps.event.trigger(map, "resize");
            // Remove the eventListener
            elem.removeEventListener('transitionend', this, false);
        });
    });
}

$('#left-panel-toggle').click(function(e) {
    perform_left_toggle();
});

function perform_right_toggle() {
    var elem = document.querySelector(".left-panel");

    //Get inital size. Animating map (right-panel)
    var collapsed = elem.getBoundingClientRect();

    elem.classList.add('expanding');

    if ($('.right-panel').hasClass('no-width')) {
        showRightPanel();
    } else {
        hideRightPanel();
        
    }

    var expanded = elem.getBoundingClientRect();

    //Invert
    var invertedTop = collapsed.top - expanded.top;
    var invertedLeft = collapsed.left - expanded.left;
    // Use divisions when manipulating sizes to apply in scale
    var invertedWidth = collapsed.width / expanded.width;
    var invertedHeight = collapsed.height / expanded.height;

    elem.style.transformOrigin = 'top left';

    elem.style.transform = 'translate(' + invertedLeft + 'px, ' + invertedTop + 'px) scale(' + invertedWidth + ', ' + invertedHeight + ')';

    requestAnimationFrame(function(){
        // Add the class to run the transition
        elem.classList.add('transition'); 
        // Clear styles
        elem.style.transform = '';
        // On transitionEnd remove the classes used control transitions
        elem.addEventListener('transitionend', function(){
            elem.style.transformOrigin = '';
            elem.classList.remove('transition');
            elem.classList.remove('expanding');
            //trigger map resize on animation complete
            google.maps.event.trigger(map, "resize");
            // Remove the eventListener
            elem.removeEventListener('transitionend', this, false);
        });
    }); 

    $('.gallery-menu-items').hide();
}

$('#right-panel-toggle').click(function(e) {
    perform_right_toggle();
});

function activateSnackbar(snackbarDiv) {
    $(snackbarDiv).addClass('show');
    setTimeout(function() {
        $(snackbarDiv).removeClass('show');
    }, 3000);
}

