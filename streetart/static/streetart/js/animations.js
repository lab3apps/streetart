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
                    $('#alt-images-card').append('<div id="alt-image" class="col-md-3"><img class="img-responsive" src="' + art.altImages[key] + '"></div>');
            }
        } else {
            $('#images-card-holder').empty();
        }
    }
}

function markerClicked() {
    if(viewState === 0) {
        expandMap();
    }
}

function backClicked() {
    if(viewState === 1){
        colapseMap();
    } else if (viewState === 2) {
        colapseCard();
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
    viewState = 1;
}

function colapseMap() {
    focusLeft();
    $('#marker-card-holder').hide();
    $('.title-block').show();
    $('.back-block').hide();
    $('.gallery-item').removeClass('col-md-6');
    $('.gallery-item').addClass('col-md-3');
    viewState = 0;
}

function expandCard() {
    focusLeft();
    $('#comment-card-holder').show();
    $('#images-card-holder').show();
    $('#expand').hide();
    $('.scroll-gallery').hide();
    $('.left-panel').css('overflow-y', 'scroll');
    $('.image').css('height', '30%');
    viewState = 2;
}

function colapseCard() {
    focusRight();
    $('#comment-card-holder').hide();
    $('#images-card-holder').hide();
    $('#expand').show();
    $('.scroll-gallery').show();
    $('.left-panel').css('overflow-y', 'hidden');
    $('.image').css('height', '20%');
    viewState = 1;
}