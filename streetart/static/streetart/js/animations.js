/* View States:
 * 0: Default large left panel with gallery.
 * 1: Large map panel with small card and gallery.
 * 2: Large left panel with expanded Card.
 */
var viewState = 0;

/* Loads the comment section into html using ajax request with the index on clicked artwork */
function loadCommentSection(index) {
    if (arrayHasOwnIndex(artworks, index)) {
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
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        var imageArray = art.altImages.split(",")
        if(imageArray.length >= 1) {
            $('#images-card-holder').empty();
            $('#images-card-holder').append('<div id="alt-images-card" class="card"></div>');
            for(var key in imageArray) {
                    $('#alt-images-card').append('<a id="alt-image" href="' +  imageArray[key] + '" data-lightbox="lightbox" class="col-xs-3"><img class="img-responsive" src="' + art.altImages[key] + '"></a>');
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
    // Hide image while other loads. This will break linking.
    //$('.main-image').attr('src', '');
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    showLeftPanel();
}

function backClicked() {
    if(viewState === 1){
        collapseMap();
        history.replaceState({}, null, '/');
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
    $('.tab-block').hide();
    $('.gallery-item').removeClass('col-md-3');
    $('.getinvolved-item').removeClass('col-md-3');
    $('.gallery-item').addClass('col-md-6');
    $('.getinvolved-item').addClass('col-md-6');
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
    $('.tab-block').show();
    $('.gallery-item').removeClass('col-md-6');
    $('.getinvolved-item').removeClass('col-md-6');
    $('.gallery-item').addClass('col-md-3');
    $('.getinvolved-item').addClass('col-md-3');
    // Important for mobile
    $('.left-panel').removeClass('mobile-hide');
    $('.right-panel').addClass('mobile-hide');
    $('#nearest-artworks-holder').hide();
    viewState = 0;
}

function expandCard() {
    focusLeft();
    $('#comment-card-holder').show();
    $('#images-card-holder').show();
    $('.scroll-gallery').hide();
    $('.left-panel').css('overflow-y', 'scroll');
    $('.main-image').addClass('expanded');
    $(".card-details").slideDown();
    $('.overlay-title').fadeOut();
    $('.overlay-like').fadeOut();
    $('.overlay-checkin').fadeOut();
    $('.overlay-expand').addClass('rotate-180');
    $('.overlay-expand').attr('onclick', 'collapseCard()');
    $('.card-image-link').attr('onclick', 'collapseCard()');
    $('#nearest-artworks-holder').hide();
    viewState = 2;
}

function collapseCard() {
    focusRight();
    $('#comment-card-holder').hide();
    $('#images-card-holder').hide();
    $('.scroll-gallery').show();
    $('.left-panel').css('overflow-y', 'hidden');
    $('.main-image').removeClass('expanded');
    $(".card-details").slideUp();
    $('.overlay-title').fadeIn();
    $('.overlay-like').fadeIn();
    $('.overlay-checkin').fadeIn();
    $('.overlay-expand').removeClass('rotate-180');
    $('.overlay-expand').attr('onclick', 'expandCard()');
    $('.card-image-link').attr('onclick', 'expandCard()');
    $('#nearest-artworks-holder').show();
    viewState = 1;
}

function hideLeftPanel() {
    //$('.left-panel').addClass('no-width');
    $('.right-panel').addClass('full-width');
    $('.left-panel').blindLeftOut('slow');
    $('#left-panel-toggle').addClass('rotate-180');
    $('.left-panel').css('border-right', 'none');
}

function showLeftPanel() {
    //$('.left-panel').removeClass('no-width');
    $('.right-panel').removeClass('full-width');
    $('.left-panel').blindLeftIn('slow');
    $('#left-panel-toggle').removeClass('rotate-180');
    $('.left-panel').css('border-right', 'solid 3px black');
}

function resizeMap() {
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
}

$('#left-panel-toggle').click(function(e) {
    if ($('.right-panel').hasClass('full-width')) {
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

$('#gallery-tab').click(function() {
    showGalleryTab();
});


$('#getinvolved-tab').click(function() {
    showGetInvolvedTab();
});


$('#whatsnew-tab').click(function() {
    showWhatsNewTab();
});

function showGalleryTab() {
    $('.getinvolved-section').hide();
    $('.whatsnew-section').hide();
    $('.gallery-section').show();
    $('#gallery-tab').addClass('active');
    $('#getinvolved-tab').removeClass('active');
    $('#whatsnew-tab').removeClass('active');
}

function showGetInvolvedTab() {
    $('.getinvolved-section').show();
    $('.gallery-section').hide();
    $('.whatsnew-section').hide();
    $('#getinvolved-tab').addClass('active');
    $('#gallery-tab').removeClass('active');
    $('#whatsnew-tab').removeClass('active');
}

function showWhatsNewTab() {
    $('.whatsnew-section').show();
    $('.gallery-section').hide();
    $('.getinvolved-section').hide();
    $('#whatsnew-tab').addClass('active');
    $('#gallery-tab').removeClass('active');
    $('#getinvolved-tab').removeClass('active');
}

