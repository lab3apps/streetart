var map;
var markerCluster
function initialize() {
    var mapDiv = document.getElementById("map");
    map = new google.maps.Map(
        mapDiv, {
            center: new google.maps.LatLng(-43.5314, 172.6365),
            zoom: 14,
            maxZoom: 20,
            minZoom: 12,
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
            fullscreenControl: false,
            styles: [
                {
                    "featureType": "all",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "weight": "2.00"
                        }
                    ]
                },
                {
                    "featureType": "all",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        {
                            "color": "#9c9c9c"
                        }
                    ]
                },
                {
                    "featureType": "all",
                    "elementType": "labels.text",
                    "stylers": [
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "all",
                    "stylers": [
                        {
                            "color": "#f2f2f2"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "landscape.man_made",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "all",
                    "stylers": [
                        {
                            "saturation": -100
                        },
                        {
                            "lightness": 45
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#eeeeee"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#7b7b7b"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "simplified"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.icon",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": [
                        {
                            "color": "#46bcec"
                        },
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#c8d7d4"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#070707"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                }
            ]
        });
    //map.mapTypes.set(layerID, layer);
    markerCluster = new MarkerClusterer(map, markers,
            {imagePath: '/static/img/cluster'});
    markerCluster.setMaxZoom(16);
    addMarkers();
    //preloadImages();
    //google.maps.event.addListenerOnce(map, 'tilesloaded', addMarkers);

    infoWindow = new google.maps.InfoWindow;
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        markerUrl = '/static/img/location-marker.png';
        var location = new google.maps.Marker({
            id: 'location',
            position: pos,
            map: map,
            icon: markerUrl
        });
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    /*infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);*/
    console.log(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
}

function addMarkers() {
    for(var key in artworks) {
        if (arrayHasOwnIndex(artworks, key)) {
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
            var marker_content = '';
            for(var a_index in art.artists) {
                if (arrayHasOwnIndex(art.artists, a_index)) {
                    if (marker_content != '') {
                        marker_content += ', ';
                    }
                    marker_content += art.artists[a_index];
                }
            }
            if (art.title !== "") {
                marker_content = '"' + art.title + '"<br>' + marker_content;
            }
            if (marker_content === '') {
                marker_content = 'Unknown';
            }

            markers[key] = marker;
            markerCluster.addMarker(marker);

            google.maps.event.addListener(marker, 'mouseover', function () {
                //this['infowindow'].open(map, this);
            });
            google.maps.event.addListener(marker, 'click', function () {
                focusOnMarker(this.id);
                panToPointIfNeeded(this.id);
                //markerClicked();
                //getNearestArtworks(this.id)
            });
            google.maps.event.addListener(marker, 'mouseout', function () {
                //this['infowindow'].close(map, this);
            });
        }
    }
}

function closeMarkers() {
    for(var key in markers) {
        if (arrayHasOwnIndex(markers, key)) {
            var marker = markers[key];
            marker['infowindow'].close(map, marker);
        }
    }
}

function preloadImages() {
    for(var key in artworks) {
        if (arrayHasOwnIndex(artworks, key)) {
            var art = artworks[key];
            //$('<img />').attr('src',art.imageUrl).appendTo('body').css('display','none');

            var imgPreload = new Image();
            imgPreload.src = art.imageUrl;
            if (imgPreload.complete || imgPreload.readyState === 4) {
                art.image = imgPreload;
            } else {
                $(imgPreload).on('load', function() {
                    /*images[key] = imgPreload;
                    console.log(images[key]);*/
                });
            }
        }
    }
}

function filterMarkers() {
    var searchText = $('#search-input').val();
    var catArray = $("input[name='status']:checked").map(function(){
        return $(this).val();
      }).get();
    console.log(catArray);
    markerCluster.clearMarkers();
    for(var key in artworks) {
        if (arrayHasOwnIndex(artworks, key)) {
            var art = artworks[key];
            var marker = markers[key];
            if ((art.title.toLowerCase().indexOf(searchText.toLowerCase()) >= 0 ||
                art.description.toLowerCase().indexOf(searchText.toLowerCase()) >= 0) &&
                catArray.indexOf(art.status) >= 0) {
                marker.setVisible(true);
                markerCluster.addMarker(marker);
                $('#artbox-'+key).show();
            } else {
                marker.setVisible(false);
                markerCluster.removeMarker(marker);
                $('#artbox-'+key).hide();
            }
            if(art.artists.length >= 1) {
                var artist_found = false;
                for(var artist_key in art.artists) {
                    if (arrayHasOwnIndex(art.artists, artist_key)) {
                        if (art.artists[artist_key]['name'].toLowerCase().indexOf(searchText.toLowerCase()) >= 0 &&
                            catArray.indexOf(art.status) >= 0) {
                            artist_found = true;
                            marker.setVisible(true);
                            markerCluster.addMarker(marker);
                            $('#artbox-'+key).show();
                        }
                    }
                }
                if (!artist_found) {
                    marker.setVisible(false);
                    markerCluster.removeMarker(marker);
                    $('#artbox-'+key).hide();
                }
            }
        }
    }
    $('.thumbnail-image').scroll();
}

var currentBounceMarker;
function toggleBounce(marker) {
    console.log('togglebounce');
    if (currentBounceMarker) {
        if(currentBounceMarker != marker){
            currentBounceMarker.setAnimation(null);
        }
        currentBounceMarker = marker;
        currentBounceMarker.setAnimation(google.maps.Animation.BOUNCE);
        
    }else{
        currentBounceMarker = marker;
        currentBounceMarker.setAnimation(google.maps.Animation.BOUNCE);
    }
 }



$( document ).ready(function() {
    initialize();
    $('#search-input').keyup(function() {
        filterMarkers();
    });

    $('.checkbox-form input').click(function() {
        filterMarkers();
    });

});


