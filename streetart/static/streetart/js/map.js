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
    google.maps.event.addListenerOnce(map, 'tilesloaded', addMarkers);
}

function addMarkers() {
    var count = 1;
    for(var key in artworks) {
        if (artworks.hasOwnProperty(key)) {
            var art = artworks[key];
            var point = new google.maps.LatLng(art.lat, art.lng);
            var marker = new google.maps.Marker({
                id: key,
                position: point,
                map: map,
                label: '' + count,
                animation: google.maps.Animation.DROP
            });
            marker['infowindow'] = new google.maps.InfoWindow({
                content: "<h2>" + art.name + "</h2>"
            });
            google.maps.event.addListener(marker, 'mouseover', function () {
                this['infowindow'].open(map, this);
            });
            google.maps.event.addListener(marker, 'click', function () {
                expandMap();
                focusOnMarker(this.id);
                //getNearestArtworks(this.id)
            });
            google.maps.event.addListener(marker, 'mouseout', function () {
                this['infowindow'].close(map, this);

            });
            count += 1;
        }
    }
}

function getNearestArtworks(index) {
    console.log("Ajax - Artwork requested. PK: " + index);
    $.ajax({
        url: '/streetart/getdata/' + index + '/',
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

initialize();