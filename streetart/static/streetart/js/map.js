var map;

function initialize() {
    var mapDiv = document.getElementById("map");
    var layer = "toner";
    map = new google.maps.Map(
        mapDiv, {
            center: new google.maps.LatLng(-43.5314, 172.6365),
            zoom: 14,
            maxZoom: 25,
            minZoom: 12,
            mapTypeId: layer,
            mapTypeControl: false,
            streetViewControl: true,
            zoomControl: true,
            zoomControlOptions: {
              position: google.maps.ControlPosition.RIGHT_CENTER
            },
            scaleControl: true,
            streetViewControl: true,
            streetViewControlOptions: {
              position: google.maps.ControlPosition.LEFT_TOP
            },
            fullscreenControl: true
        });
    map.mapTypes.set(layer, new google.maps.StamenMapType(layer));
    addMarkers();
    //google.maps.event.addListenerOnce(map, 'tilesloaded', addMarkers);
}

function addMarkers() {
    for(var key in artworks) {
        if (artworks.hasOwnProperty(key)) {
            var art = artworks[key];
            var markerUrl;

            if(art.status === '1') {
                markerUrl = '/static/img/visible.png';
            } else if(art.status === '2') {
                markerUrl = '/static/img/part_visible.png';
            } else if(art.status === '3') {
                markerUrl = '/static/img/not_visible.png';
            } else {
                markerUrl = 'http://maps.google.com/mapfiles/ms/micons/blue-dot.png';
            }

            var point = new google.maps.LatLng(art.lat, art.lng);
            var marker = new google.maps.Marker({
                id: key,
                position: point,
                map: map,
                icon: markerUrl,
                animation: google.maps.Animation.DROP
            });
            marker['infowindow'] = new google.maps.InfoWindow({
                content: "<p class='map-tooltip'>" + art.name + "</p>",
                disableAutoPan: true
            });

            markers[key] = marker;

            google.maps.event.addListener(marker, 'mouseover', function () {
                this['infowindow'].open(map, this);
            });
            google.maps.event.addListener(marker, 'click', function () {
                focusOnMarker(this.id);
                markerClicked();
                //getNearestArtworks(this.id)
            });
            google.maps.event.addListener(marker, 'mouseout', function () {
                this['infowindow'].close(map, this);

            });
        }
    }
}

function focusOnMarker(index) {
    if (artworks.hasOwnProperty(index)) {
        var art = artworks[index];
        var point = new google.maps.LatLng(art.lat, art.lng);
        $('.main-image').attr("src", art.imageUrl);
        $('#main-card').data('index', index);
        $('.overlay-title').html(art.name);
        $('.card-title').html(art.name);
        $('.card-description').html(art.description);
        $('.overlay-fullscreen').attr('href', art.imageUrl);
        console.log("art.hasLiked: " + art.hasLiked);
        if(art.hasLiked === 'True') {
            $('.overlay-like i').html('favorite');
        } else {
            $('.overlay-like i').html('favorite_border');
        }
        if(art.hasCheckedin === 'True') {
            $('.overlay-checkin i').addClass('palette-Green');
            $('.overlay-checkin i').removeClass('palette-White');
        } else {
            $('.overlay-checkin i').addClass('palette-White');
            $('.overlay-checkin i').removeClass('palette-Green');
        }
        $('#likeCount').html(art.likes_count);
        $('#checkinCount').html(art.checkins_count);
        $('#show_on_map').data('index', index);
        map.panTo(point);
        loadCommentSection(index);
        loadAltImages(index);
    }
}

$('#show_on_map').click(function(e) {
    $('.left-panel').addClass('mobile-hide');
    $('.right-panel').removeClass('mobile-hide');
    google.maps.event.trigger(map, "resize");
    var marker_index = $(this).data('index');
    if (artworks.hasOwnProperty(marker_index)) {
        var art = artworks[marker_index];
        var point = new google.maps.LatLng(art.lat, art.lng);
        map.panTo(point);
    }
});

function getNearestArtworks(index) {
    console.log("Ajax - Artwork requested. PK: " + index);
    $.ajax({
        url: '/getdata/' + index + '/',
        type: 'GET',
        success: function(data) {
            console.log("We got some data yo!")
            console.log(data);
        },
        failure: function() {
            console.log('Got an error dude');
        }
    });
}

$('#search-input').keyup(function() {
    filterMarkers();
});

function filterMarkers() {
    var searchText = $('#search-input').val();
    var catArray = $('.multiselect').val();
    for(var key in artworks) {
        if (artworks.hasOwnProperty(key)) {
            var art = artworks[key];
            var marker = markers[key];
            if ((art.name.toLowerCase().indexOf(searchText.toLowerCase()) >= 0 ||
                art.description.toLowerCase().indexOf(searchText.toLowerCase()) >= 0) &&
                catArray.indexOf(art.status) >= 0) {
                marker.setVisible(true);
                $('#artbox-'+key).show();
            } else {
                marker.setVisible(false);
                $('#artbox-'+key).hide();
            }
        }
    }
}

function initializeMultiSelect() {
    $('.multiselect').multiselect({
        buttonWidth: "100%",
        onInitialized: function() {
            filterMarkers();
        },
        onChange: function() {
            filterMarkers();
        }
    });
}

initialize();
initializeMultiSelect();