var map;

function initialize() {
    var mapDiv = document.getElementById("map");
    var layer = "toner";
    map = new google.maps.Map(
        mapDiv, {
            center: new google.maps.LatLng(-43.5314, 172.6365),
            zoom: 14,
            maxZoom: 18,
            minZoom: 12,
            mapTypeId: layer,
            mapTypeControl: false,
            streetViewControl: true,
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
                markerUrl = 'http://maps.google.com/mapfiles/ms/micons/green-dot.png';
            } else if(art.status === '2') {
                markerUrl = 'http://maps.google.com/mapfiles/ms/micons/orange-dot.png';
            } else if(art.status === '3') {
                markerUrl = 'http://maps.google.com/mapfiles/ms/micons/red-dot.png';
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
                content: "<h2>" + art.name + "</h2>"
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
        $('.overlay-title').html(art.name);
        $('.card-title').html(art.name);
        $('.card-description').html(art.description);
        $('.overlay-fullscreen').attr('href', art.imageUrl);
        $('#like').attr('value', index);
        $('#likeCount').html(art.likes_count);
        $('#checkin').attr('value', index);
        $('#checkinCount').html(art.checkins_count);
        $('#like').attr('value', index);
        $('#likeCount').html(art.likes_count);
        $('#checkin').attr('value', index);
        $('#checkinCount').html(art.checkins_count);
        $('#show_on_map').data('index', index);
        loadCommentSection(index);
        loadAltImages(index);
        map.panTo(point);
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