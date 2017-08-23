function focusOnMarker(index) {
    if (artworks.hasOwnProperty(index)) {
        var art = artworks[index];
        var point = new google.maps.LatLng(art.lat, art.lng);
        $('.image').attr("src", art.imageUrl);
        $('.card-title').html(art.name);
        $('.card-description').html(art.description);
        map.panTo(point);
    }
}

function expandMap() {
    $('.left-panel').removeClass('col-md-7');
    $('.left-panel').addClass('col-md-4');
    $('.right-panel').removeClass('col-md-5');
    $('.right-panel').addClass('col-md-8');
    $('.card-holder').css("display", 'block');
    $('.title-block').css("display", 'none');
    $('.back-block').css("display", 'block');
    $('.gallery-item').removeClass('col-md-3');
    $('.gallery-item').addClass('col-md-6');
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
}

function colapseMap() {
    $('.left-panel').removeClass('col-md-4');
    $('.left-panel').addClass('col-md-7');
    $('.right-panel').removeClass('col-md-8');
    $('.right-panel').addClass('col-md-5');
    $('.card-holder').css("display", 'none');
    $('.title-block').css("display", 'block');
    $('.back-block').css("display", 'none');
    $('.gallery-item').removeClass('col-md-6');
    $('.gallery-item').addClass('col-md-3');
    setTimeout(function() {
        google.maps.event.trigger(map, "resize");
    }, 300);
}