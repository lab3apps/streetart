/* View States:
 * 0: Default large left panel with gallery.
 * 1: Large map panel with small card and gallery.
 * 2: Large left panel with expanded Card.
 */
var viewState = 0;

/* Loads the comment section into html using ajax request with the index on clicked artwork */
function loadCommentSection(index) {
    if (artworks.hasOwnProperty(index)) {
        $.ajax({
            url: '/imageselected/' + index + '/',
            type: 'GET',
            success: function(data) {
                $('#comment-card').empty().append(data);
            },
            failure: function() {
                console.log('Ajax failure: unable to GET "/imageselected/' + index + '/"');
            }
        });
    }
}

/* Places any alternative images into the card holder for the clicked artwork. Empties if no alt images */
function loadAltImages(index) {
    if (artworks.hasOwnProperty(index)) {
        var art = artworks[index];
        if(art.altImages.length >= 1) {
            $('#images-card-holder').empty();
            $('#images-card-holder').append('<div id="alt-images-card" class="card"></div>');
            for(var key in art.altImages) {
                    $('#alt-images-card').append('<a id="alt-image" href="' +  art.altImages[key] + '" data-lightbox="lightbox" class="col-xs-3"><img class="img-responsive" src="' + art.altImages[key] + '"></a>');
            }
        } else {
            $('#images-card-holder').empty();
        }
    }
}

function markerClicked() {
    if(viewState === 0 || viewState === 1) {
        expandMap();
    }
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    showLeftPanel();
}

function backClicked() {
    if(viewState === 1){
        collapseMap();
    } else if (viewState === 2) {
        collapseCard();
    }
}

function focusRight() {
    $('.left-panel').removeClass('col-md-7');
    $('.left-panel').addClass('col-md-4');
    $('.right-panel').removeClass('col-md-5');
    $('.right-panel').addClass('col-md-8');
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
}

function focusLeft() {
    $('.left-panel').removeClass('col-md-4');
    $('.left-panel').addClass('col-md-7');
    $('.right-panel').removeClass('col-md-8');
    $('.right-panel').addClass('col-md-5');
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
}

function expandMap() {
    focusRight();
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
    focusLeft();
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
    focusLeft();
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
    focusRight();
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
    $('#left-panel-toggle').addClass('rotate-180');
}

function showLeftPanel() {
    $('.left-panel').removeClass('no-width');
    $('.right-panel').removeClass('full-width');
    $('#left-panel-toggle').removeClass('rotate-180');
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

function activateSnackbar(snackbarDiv) {
    $(snackbarDiv).addClass('show');
    setTimeout(function() {
        $(snackbarDiv).removeClass('show');
    }, 3000);
}
