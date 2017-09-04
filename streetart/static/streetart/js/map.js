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
    //preloadImages();
    //google.maps.event.addListenerOnce(map, 'tilesloaded', addMarkers);
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
            marker['infowindow'] = new google.maps.InfoWindow({
                content: "<p class='map-tooltip'>" + marker_content + "</p>",
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

function focusOnMarker(index) {
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        var marker = markers[index];
        closeMarkers();
        marker['infowindow'].open(map, marker);
        var point = new google.maps.LatLng(art.lat, art.lng);
        // Image Loading
        $('.loader').removeClass('none');
        if (art.image) {
            $('.loader').addClass('none');
            $('.main-image').attr('src', art.image.src);
        } else {
            var imgPreload = new Image();
            imgPreload.src = art.imageUrl;
            art.image = imgPreload;
            if (imgPreload.complete || imgPreload.readyState === 4) {
                $('.loader').addClass('none');
                $('.main-image').attr('src', imgPreload.src);
            } else {
                //$('.loader').removeClass('none');
                $(imgPreload).on('load', function(response, status, xhr) {
                    if (status == 'error') {
                        $('.loader').addClass('none');
                        console.log('Failed to load image');
                    } else {
                        $('.loader').addClass('none');
                        $('.main-image').attr('src', imgPreload.src);
                    }
                });
            }
        }
        
        
        //Used to get focused artworks id for liking and checking in.
        $('#main-card').data('index', index);
        var overlay_title = '';
        for(var key in art.artists) {
            if (arrayHasOwnIndex(art.artists, key)) {
                if (overlay_title != '') {
                    overlay_title += ', ';
                }
                overlay_title += art.artists[key];
            }
        }
        if (art.title !== "") {
            overlay_title = '"' + art.title + '"<br>' + overlay_title;
        }
        if (overlay_title === ''){
            $('.overlay-title').addClass('none');
        } else {
            $('.overlay-title').removeClass('none');
            $('.overlay-title').html(overlay_title);
        }
        $('.card-title').html(art.title);
        $('.card-description').html(art.description);
        if(art.commission_date !== 'None') {
            $('.card-commission').show();
            $('.commission-date').html(art.commission_date);
        } else {
            $('.card-commission').hide();
        }
        if(art.decommission_date !== 'None') {
            $('.card-decommission').show();
            $('.decommission-date').html(art.decommission_date);
        } else {
            $('.decard-commission').hide();
        }

        if(art.artists.length >= 1) {
            var artistsNames = $('.artists-names');
            artistsNames.empty();
            for(var key in art.artists) {
                if (arrayHasOwnIndex(art.artists, key)) {
                    artistsNames.append(art.artists[key]);
                    if(!(key == art.artists.length - 1)) {
                        artistsNames.append(', ');
                    }
                }
            }
        } else {
            $('.artists-names').empty();
        }

        $('.overlay-fullscreen').attr('href', art.imageUrl);
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
    if (arrayHasOwnIndex(artworks, marker_index)) {
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
        if (arrayHasOwnIndex(artworks, key)) {
            var art = artworks[key];
            var marker = markers[key];
            if ((art.title.toLowerCase().indexOf(searchText.toLowerCase()) >= 0 ||
                art.description.toLowerCase().indexOf(searchText.toLowerCase()) >= 0) &&
                catArray.indexOf(art.status) >= 0) {
                marker.setVisible(true);
                $('#artbox-'+key).show();
            } else if(art.artists.length >= 1) {
                var artist_found = false;
                for(var key in art.artists) {
                    if (arrayHasOwnIndex(art.artists, key)) {
                        if (art.artists[key].toLowerCase().indexOf(searchText.toLowerCase()) >= 0 &&
                            catArray.indexOf(art.status) >= 0) {
                            artist_found = true;
                            marker.setVisible(true);
                            $('#artbox-'+key).show();
                        }
                    }
                }
                if (!artist_found) {
                    marker.setVisible(false);
                    $('#artbox-'+key).hide();
                }
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