var map;
var markerCluster
function initialize() {
    PopulateArtworks();
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


    markerCluster = new MarkerClusterer(map, markers,
            {imagePath: '/static/img/cluster'});
    markerCluster.setMaxZoom(16);

    google.maps.event.addListenerOnce(map, 'tilesloaded', addMarkers);

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

function focusOnMarker(index) {

        var art = artworks[index];
        var marker = markers[index];
        getNearestArtworks(index)
        $('#nearest-artworks-holder').show();

        var images = artworks[index].altImages.split(",");

        $.each(images, function(index,obj) {
            var imgtag = '<img class="thumbnail-image" src="' + obj + '"/>';
            $('#alt-images-card').append(imgtag);
        });
        if(images.length >=1)
        {
            $('#images-card-holder').show();
        }else
        {
            $('#images-card-holder').hide();
        }

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
        var artists_text = '';
        var artists_bio_html = '';
        for(var key in art.artists) {
            if (arrayHasOwnIndex(art.artists, key)) {
                if (artists_text != '') {
                    artists_text += ', ';
                }
                artists_text += art.artists[key]['name'];
                artists_bio_html += '<br><div>';
                if (art.artists[key]['name'] && art.artists[key]['name'] != '' && art.artists[key]['name'] != 'None'){
                    artists_bio_html += '<span>'+art.artists[key]['name']+'</span><br>';
                }
                if (art.artists[key]['biography'] && art.artists[key]['biography'] != '' && art.artists[key]['biography'] != 'None'){
                    artists_bio_html += '<span>'+art.artists[key]['biography']+'</a> </span><br>';
                }
                if (art.artists[key]['website'] && art.artists[key]['website'] != '' && art.artists[key]['website'] != 'None'){
                    artists_bio_html += '<span><a href="'+art.artists[key]['website']+'">'+art.artists[key]['website']+'</a> </span><br>';
                }
                if (art.artists[key]['facebook'] && art.artists[key]['facebook'] != '' &&  art.artists[key]['facebook'] != 'None'){
                    if (art.artists[key]['facebook'].indexOf('facebook.com') !== -1) {
                        artists_bio_html += '<span><a href="'+art.artists[key]['facebook']+'">'+'<i class="icon fa fa-facebook-official"></i>'+'  '+art.artists[key]['name']+'</a> </span><br>';
                    } else {
                        artists_bio_html += '<span><a href="https://www.facebook.com/'+art.artists[key]['facebook']+'">'+'<i class="icon fa fa-facebook-official"></i>'+'  '+art.artists[key]['name']+'</a> </span><br>';
                    }
                }
                if (art.artists[key]['instagram'] && art.artists[key]['instagram'] != '' && art.artists[key]['instagram'] != 'None'){
                    var insta_index = art.artists[key]['instagram'].indexOf('instagram.com/');
                    if (insta_index !== -1) {
                        artists_bio_html += '<a href="'+art.artists[key]['instagram']+'"><i class="icon fa fa-instagram"></i>'+'  @'+art.artists[key]['instagram'].split('instagram.com/')[1].replace('/', '')+'</a> </span><br>';
                    } else {
                        artists_bio_html += '<a href="https://www.instagram.com/'+art.artists[key]['instagram']+'"><i class="icon fa fa-instagram"></i>'+'  @'+art.artists[key]['instagram']+'</a> </span><br>';
                    }
                }
                if (art.artists[key]['twitter'] && art.artists[key]['twitter'] != '' && art.artists[key]['twitter'] != 'None'){
                    var twitter_index = art.artists[key]['twitter'].indexOf('twitter.com/');
                    if (twitter_index !== -1) {
                        artists_bio_html += '<span><a href="'+art.artists[key]['twitter']+'">'+'<i class="icon fa fa-twitter"></i>'+'  @'+art.artists[key]['twitter'].split('twitter.com/')[1].replace('/', '')+'</a> </span><br>';
                    } else {
                        artists_bio_html += '<span><a href="https://www.twitter.com/'+art.artists[key]['twitter']+'">'+'<i class="icon fa fa-twitter"></i>'+'  @'+art.artists[key]['twitter']+'</a> </span><br>';
                    }
                }
                artists_bio_html += '</div>';
            }
        }
        console.dir(art);

        /*for(var key in art.crews) {
            if (arrayHasOwnIndex(art.artists, key)) {
                if (artists_text != '') {
                    artists_text += ', ';
                }
                artists_text += art.artists[key]['name'];
                artists_bio_html += '<br><div>';
            }
        }*/

        $("#card-content").html('');

        var overlay_title = '';
        if (artists_text !== "") {
            overlay_title = artists_text;
        }
        if (overlay_title === ''){
            $('.overlay-title').addClass('none');
        } else {
            $('.overlay-title').removeClass('none');
            $('.overlay-title').html(overlay_title);
        }
        if (art.title != "") {
            $("#card-content").append('<p class="card-title">\
                <span class="artwork-title">'+art.title+'</span>\
            </p>');
        }
        if (artists_text != "") {
            $("#card-content").append('<p class="card-artists">\
                <span class="artwork-artists">'+artists_text+'</span>\
            </p>');
        }
        if (art.description != "") {
            $("#card-content").append('<p class="card-description">\
                <span class="artwork-description">'+art.description+'</span>\
            </p>');
        }

        for(var key in art) {
            if (art[key] != 'None' && art[key] != '') {
                if (key == 'commission_date' || key == 'decommission_date') {
                    $("#card-content").append('<p class="card-generated">\
                        <span class="value-title">'+key.replace('_', ' ')+': </span>\
                        <span class="artwork-'+key+'">'+art[key]+'</span>\
                    </p>');
                } else if (key == 'link') {
                    $("#card-content").append('<p class="card-generated">\
                        <span class="value-title">'+key.replace('_', ' ')+': </span>\
                        <span class="artwork-'+key+'"><a href="'+art[key]+'">'+art[key]+'</a></span>\
                    </p>');
                }
            }
        }
        $("#card-content").append(artists_bio_html);
        $('.overlay-fullscreen').attr('href', art.imageUrl);
        if(art.hasLiked === 'True') {
            $('.like i').html('favorite');
        } else {
            $('.like i').html('favorite_border');
        }
        if(art.hasCheckedin === 'True') {
            $('.checkin-icon-unfilled').hide();
            $('.checkin-icon-filled').show();
        } else {
            $('.checkin-icon-filled').hide();
            $('.checkin-icon-unfilled').show();
        }
        $('#likeCount').html(art.likes_count);
        if (art.likes_count != 1) {
            $('#like-plural').show();
        } else {
            $('#like-plural').hide();
        }
        $('#checkinCount').html(art.checkins_count);
        if (art.checkins_count != 1) {
            $('#checkin-plural').show();
        } else {
            $('#checkin-plural').hide();
        }
        $('#show_on_map').data('index', index);
        map.panTo(point);
        map.setZoom(17);
        toggleBounce(marker);
        loadCommentSection(index);
        loadAltImages(index);
        history.replaceState({}, null, '/artwork/'+index);

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
    $.ajax({
        async:'true',
        url: '/nearby/' + index + '/',
        type: 'GET',
        success: function(response) {
            RenderNearestArtworks(response,index);
        },
        failure: function(error) {
            console.error(error);
        }
    });
}

function RenderNearestArtworks(response,_index){
    if(viewState===1 || viewState===2)
    {
        //res =  jQuery.parseJSON( response );
        $("#nearest-artworks-holder").html("");
        var no_of_nearest = response.length-1;
        var elements_in_row = 4;
        var height_of_row =109;    //px
        var no_of_rows = Math.floor(no_of_nearest/elements_in_row);
        if(no_of_nearest%elements_in_row>0)
        {
        no_of_rows++;
        }

        console.log(no_of_rows);
        //$("#nearest-artworks-holder").height( no_of_rows * height_of_row);
        $.each(response, function (index,obj)
        {
         if(_index!=obj.pk)
         {
           var imagetag ;
            if(obj.imageUrl)
            {
            imagetag = '<img class="lazy thumbnail-image" src="'+obj.imageUrl+'" >';
            }

            var view ='<div id="artbox-'+obj.pk+'" class="gallery-item col-xs-6 col-sm-3 col-md-3">'+
                        '<div class="dummy"></div>'+
                        '<a class="img-link" onclick="focusOnMarker('+obj.pk+'), markerClicked()">'+ imagetag+
                        '</a>'+
                    '</div>';
            $("#nearest-artworks-holder").append(view);
         }
        });
    }
}

$('#search-input').keyup(function() {
    filterMarkers();
});

function filterMarkers() {
    var searchText = $('#search-input').val();
    var catArray = $('.multiselect').val();
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
    if (currentBounceMarker) {
        if (currentBounceMarker.getAnimation() !== null) {
          currentBounceMarker.setAnimation(null);
        } 
        currentBounceMarker = marker;
        currentBounceMarker.setAnimation(google.maps.Animation.BOUNCE);
    }else{
        currentBounceMarker = marker;
        currentBounceMarker.setAnimation(google.maps.Animation.BOUNCE);
    }
 }       

function initializeMultiSelect() {
    $('.multiselect').multiselect({
        buttonText: function(options, select) {
                return 'Show artworks that are';
            },
        buttonWidth: "100%",
        onInitialized: function() {
            filterMarkers();
        },
        onChange: function() {
            filterMarkers();
        }
    });
}



$( document ).ready(function() {
    initializeMultiSelect();
    $('#search-input').keyup(function() {
        filterMarkers();
    });

});


