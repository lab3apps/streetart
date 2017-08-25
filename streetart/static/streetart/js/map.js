var map;

function initialize() {
    var mapDiv = document.getElementById("map");
    var layer = "toner";
    map = new google.maps.Map(
        mapDiv, {
            center: new google.maps.LatLng(-43.5314, 172.6365),
            zoom: 12,
            maxZoom: 18,
            minZoom: 12,
            mapTypeId: layer,
            mapTypeControlOptions: {
                mapTypeIds: [layer]
            }
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
                markerClicked();
                focusOnMarker(this.id);
                //getNearestArtworks(this.id)
            });
            google.maps.event.addListener(marker, 'mouseout', function () {
                this['infowindow'].close(map, this);

            });
        }
    }
    console.log(markers);
}

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