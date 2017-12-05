function get_artist_bio(art) {
    var artists_text = '';
    var artists_bio_html = '';
    for (var key in art.artists) {
        if (arrayHasOwnIndex(art.artists, key)) {
            if (artists_text != '') {
                artists_text += ', ';
            }
            artists_text += art.artists[key]['name'];
            artists_bio_html += '<br><div>';
            if (art.artists[key]['name'] && art.artists[key]['name'] != '' && art.artists[key]['name'] != 'None') {
                artists_bio_html += '<span>' + art.artists[key]['name'] + '</span><br>';
            }
            if (art.artists[key]['biography'] && art.artists[key]['biography'] != '' && art.artists[key]['biography'] != 'None') {
                artists_bio_html += '<span>' + art.artists[key]['biography'] + '</a> </span><br>';
            }
            if (art.artists[key]['website'] && art.artists[key]['website'] != '' && art.artists[key]['website'] != 'None') {
                artists_bio_html += '<span><a href="' + art.artists[key]['website'] + '">' + art.artists[key]['website'] + '</a> </span><br>';
            }
            if (art.artists[key]['facebook'] && art.artists[key]['facebook'] != '' && art.artists[key]['facebook'] != 'None') {
                if (art.artists[key]['facebook'].indexOf('facebook.com') !== -1) {
                    artists_bio_html += '<span><a href="' + art.artists[key]['facebook'] + '">' + '<i class="icon fa fa-facebook-official"></i>' + '  ' + art.artists[key]['name'] + '</a> </span><br>';
                } else {
                    artists_bio_html += '<span><a href="https://www.facebook.com/' + art.artists[key]['facebook'] + '">' + '<i class="icon fa fa-facebook-official"></i>' + '  ' + art.artists[key]['name'] + '</a> </span><br>';
                }
            }
            if (art.artists[key]['instagram'] && art.artists[key]['instagram'] != '' && art.artists[key]['instagram'] != 'None') {
                var insta_index = art.artists[key]['instagram'].indexOf('instagram.com/');
                if (insta_index !== -1) {
                    artists_bio_html += '<a href="' + art.artists[key]['instagram'] + '"><i class="icon fa fa-instagram"></i>' + '  @' + art.artists[key]['instagram'].split('instagram.com/')[1].replace('/', '') + '</a> </span><br>';
                } else {
                    artists_bio_html += '<a href="https://www.instagram.com/' + art.artists[key]['instagram'] + '"><i class="icon fa fa-instagram"></i>' + '  @' + art.artists[key]['instagram'] + '</a> </span><br>';
                }
            }
            if (art.artists[key]['twitter'] && art.artists[key]['twitter'] != '' && art.artists[key]['twitter'] != 'None') {
                var twitter_index = art.artists[key]['twitter'].indexOf('twitter.com/');
                if (twitter_index !== -1) {
                    artists_bio_html += '<span><a href="' + art.artists[key]['twitter'] + '">' + '<i class="icon fa fa-twitter"></i>' + '  @' + art.artists[key]['twitter'].split('twitter.com/')[1].replace('/', '') + '</a> </span><br>';
                } else {
                    artists_bio_html += '<span><a href="https://www.twitter.com/' + art.artists[key]['twitter'] + '">' + '<i class="icon fa fa-twitter"></i>' + '  @' + art.artists[key]['twitter'] + '</a> </span><br>';
                }
            }
            artists_bio_html += '</div>';
        }
    }
    var bio_html = '';
    $('.overlay-title').addClass('none');
    /* var overlay_title = '';
     if (artists_text !== "") {
         overlay_title = artists_text;
     }
     if (overlay_title === ''){

     } else {
         $('.overlay-title').removeClass('none');
         $('.overlay-title').html(overlay_title);
     }*/
    if (art.title != "") {
        bio_html += '<p class="card-title">\
            <span class="artwork-title">' + art.title + '</span>\
        </p>';
    }
    if (artists_text != "") {
        bio_html += '<p class="card-artists">\
            <span class="artwork-artists">' + artists_text + '</span>\
        </p>';
    }
    if (art.description != "") {
        bio_html += '<p class="card-description">\
            <span class="artwork-description">' + art.description + '</span>\
        </p>';
    }

    for (var key in art) {
        if (art[key] != 'None' && art[key] != '') {
            if (key == 'commission_date' || key == 'decommission_date') {
                bio_html += '<p class="card-generated">\
                    <span class="value-title">' + key.replace('_', ' ') + ': </span>\
                    <span class="artwork-' + key + '">' + art[key] + '</span>\
                </p>';
            } else if (key == 'link') {
                bio_html += '<p class="card-generated">\
                    <span class="value-title">' + key.replace('_', ' ') + ': </span>\
                    <span class="artwork-' + key + '"><a href="' + art[key] + '">' + art[key] + '</a></span>\
                </p>';
            }
        }
    }
    bio_html += artists_bio_html;

    $("#card-content").html(bio_html);
    //return artists_text, artists_bio_html
}

function load_artwork_main_image(art) {
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
            $(imgPreload).on('load', function (response, status, xhr) {
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
}

function image_selected(index, init=false) {
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        var marker = markers[index];
        var point = new google.maps.LatLng(art.lat, art.lng);
        // Image Loading
        load_artwork_main_image(art);
        var artist_text, bio_html = get_artist_bio(art);
        if (map && !init) {
            map.panTo(point);
            map.setZoom(17);
        }

        toggleBounce(marker);
        loadCommentSection(index);
        loadAltImages(index);
        history.replaceState({}, null, '/artwork/' + index);
        full_card_view();
    }
}

function focusOnMarker(index) {
    image_selected(index);
    return;

    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        var marker = markers[index];
        getNearestArtworks(index)

        //if hidden
        $('#nearest-artworks-holder').show();


        //closeMarkers();
        //marker['infowindow'].open(map, marker);
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
                $(imgPreload).on('load', function (response, status, xhr) {
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
        for (var key in art.artists) {
            if (arrayHasOwnIndex(art.artists, key)) {
                if (artists_text != '') {
                    artists_text += ', ';
                }
                artists_text += art.artists[key]['name'];
                artists_bio_html += '<br><div>';
                if (art.artists[key]['name'] && art.artists[key]['name'] != '' && art.artists[key]['name'] != 'None') {
                    artists_bio_html += '<span>' + art.artists[key]['name'] + '</span><br>';
                }
                if (art.artists[key]['biography'] && art.artists[key]['biography'] != '' && art.artists[key]['biography'] != 'None') {
                    artists_bio_html += '<span>' + art.artists[key]['biography'] + '</a> </span><br>';
                }
                if (art.artists[key]['website'] && art.artists[key]['website'] != '' && art.artists[key]['website'] != 'None') {
                    artists_bio_html += '<span><a href="' + art.artists[key]['website'] + '">' + art.artists[key]['website'] + '</a> </span><br>';
                }
                if (art.artists[key]['facebook'] && art.artists[key]['facebook'] != '' && art.artists[key]['facebook'] != 'None') {
                    if (art.artists[key]['facebook'].indexOf('facebook.com') !== -1) {
                        artists_bio_html += '<span><a href="' + art.artists[key]['facebook'] + '">' + '<i class="icon fa fa-facebook-official"></i>' + '  ' + art.artists[key]['name'] + '</a> </span><br>';
                    } else {
                        artists_bio_html += '<span><a href="https://www.facebook.com/' + art.artists[key]['facebook'] + '">' + '<i class="icon fa fa-facebook-official"></i>' + '  ' + art.artists[key]['name'] + '</a> </span><br>';
                    }
                }
                if (art.artists[key]['instagram'] && art.artists[key]['instagram'] != '' && art.artists[key]['instagram'] != 'None') {
                    var insta_index = art.artists[key]['instagram'].indexOf('instagram.com/');
                    if (insta_index !== -1) {
                        artists_bio_html += '<a href="' + art.artists[key]['instagram'] + '"><i class="icon fa fa-instagram"></i>' + '  @' + art.artists[key]['instagram'].split('instagram.com/')[1].replace('/', '') + '</a> </span><br>';
                    } else {
                        artists_bio_html += '<a href="https://www.instagram.com/' + art.artists[key]['instagram'] + '"><i class="icon fa fa-instagram"></i>' + '  @' + art.artists[key]['instagram'] + '</a> </span><br>';
                    }
                }
                if (art.artists[key]['twitter'] && art.artists[key]['twitter'] != '' && art.artists[key]['twitter'] != 'None') {
                    var twitter_index = art.artists[key]['twitter'].indexOf('twitter.com/');
                    if (twitter_index !== -1) {
                        artists_bio_html += '<span><a href="' + art.artists[key]['twitter'] + '">' + '<i class="icon fa fa-twitter"></i>' + '  @' + art.artists[key]['twitter'].split('twitter.com/')[1].replace('/', '') + '</a> </span><br>';
                    } else {
                        artists_bio_html += '<span><a href="https://www.twitter.com/' + art.artists[key]['twitter'] + '">' + '<i class="icon fa fa-twitter"></i>' + '  @' + art.artists[key]['twitter'] + '</a> </span><br>';
                    }
                }
                artists_bio_html += '</div>';
            }
        }

        $("#card-content").html('');

        var overlay_title = '';
        if (artists_text !== "") {
            overlay_title = artists_text;
        }
        if (overlay_title === '') {
            $('.overlay-title').addClass('none');
        } else {
            $('.overlay-title').removeClass('none');
            $('.overlay-title').html(overlay_title);
        }
        if (art.title != "") {
            $("#card-content").append('<p class="card-title">\
                <span class="artwork-title">' + art.title + '</span>\
            </p>');
        }
        if (artists_text != "") {
            $("#card-content").append('<p class="card-artists">\
                <span class="artwork-artists">' + artists_text + '</span>\
            </p>');
        }
        if (art.description != "") {
            $("#card-content").append('<p class="card-description">\
                <span class="artwork-description">' + art.description + '</span>\
            </p>');
        }

        for (var key in art) {
            if (art[key] != 'None' && art[key] != '') {
                if (key == 'commission_date' || key == 'decommission_date') {
                    $("#card-content").append('<p class="card-generated">\
                        <span class="value-title">' + key.replace('_', ' ') + ': </span>\
                        <span class="artwork-' + key + '">' + art[key] + '</span>\
                    </p>');
                } else if (key == 'link') {
                    $("#card-content").append('<p class="card-generated">\
                        <span class="value-title">' + key.replace('_', ' ') + ': </span>\
                        <span class="artwork-' + key + '"><a href="' + art[key] + '">' + art[key] + '</a></span>\
                    </p>');
                }
            }
        }
        $("#card-content").append(artists_bio_html);
        $('.overlay-fullscreen').attr('href', art.imageUrl);
        if (art.hasLiked === 'True') {
            $('.like i').html('favorite');
        } else {
            $('.like i').html('favorite_border');
        }
        if (art.hasCheckedin === 'True') {
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
        history.replaceState({}, null, '/artwork/' + index);

        //setTimeout(function(){ expandCard(); }, 10);


    }
}

$('#show_on_map').click(function (e) {
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
    if (csrftoken !== null || csrftoken !== '' || typeof(csrftoken) !== 'undefined') {
        $.ajax({
            async: 'true',
            url: '/nearby/' + index + '/',
            data: {'csrfmiddlewaretoken': csrftoken},
            type: 'GET',
            success: function (response) {
                console.log(response);
                RenderNearestArtworks(response, index);
            },
            failure: function (error) {
                console.error(error);
            }
        });
    }
}

function RenderNearestArtworks(response, _index) {
    if (viewState === 1 || viewState === 2) {
        res = jQuery.parseJSON(response);
        $("#nearest-artworks-holder").html("");
        var no_of_nearest = res.length - 1;
        var elements_in_row = 4;
        var height_of_row = 109;    //px
        var no_of_rows = Math.floor(no_of_nearest / elements_in_row);
        if (no_of_nearest % elements_in_row > 0) {
            no_of_rows++;
        }

        console.log(no_of_rows);
        //$("#nearest-artworks-holder").height( no_of_rows * height_of_row);
        $.each(res, function (index, obj) {
            if (_index != obj.pk) {
                console.log(obj);
                var imagetag;
                if (obj.fields.cropped_image == "") {
                    imagetag = '<img class="lazy thumbnail-image" src="/media/' + obj.fields.image + '" >';
                } else {
                    imagetag = '<img class="lazy thumbnail-image" src="/media/' + obj.fields.cropped_image + '" >';
                }

                var view = '<div id="artbox-' + obj.pk + '" class="gallery-item col-xs-6 col-sm-3 col-md-3">' +
                    '<div class="dummy"></div>' +
                    '<a class="img-link" onclick="focusOnMarker(' + obj.pk + ')">' + imagetag +
                    '</a>' +
                    '</div>';
                $("#nearest-artworks-holder").append(view);
            }
        });
    }
}


/* Loads the comment section into html using ajax request with the index on clicked artwork */
function loadCommentSection(index) {
    if (arrayHasOwnIndex(artworks, index)) {
        $.ajax({
            url: '/imageselected/' + index + '/',
            type: 'GET',
            success: function (data) {
                $('#comment-card').empty().append(data);
            },
            failure: function () {
                console.log('Ajax failure: unable to GET "/imageselected/' + index + '/"');
            }
        });
    }
}

/* Places any alternative images into the card holder for the clicked artwork. Empties if no alt images */
function loadAltImages(index) {
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];

         var images = artworks[index].altImages.split(",");
        $('#alt-images-card').empty();
        $.each(images, function(index,obj) {
            var imgtag = '<img class="lazy thumbnail-image" data-src="' + obj + '"/>';

            var view = '<div id="artbox-' + art.pk + '" class="gallery-item col-xs-6 col-sm-3 col-md-3">' +
                '<div class="dummy"></div>' +
                '<a class="img-link">' + imgtag +
                '</a>' +
                '</div>';

            $('#alt-images-card').append(view);

        });
        if(images.length >=1)
        {
            $('#images-card-holder').show();
        }else
        {
            $('#images-card-holder').hide();
        }
    }
    LazyLoad();
}

function LazyLoad() {
            $('.lazy').lazy({
                scrollDirection: 'vertical',
                effect: 'fadeIn',
                beforeLoad: function (element) {
                    // called before an elements gets handled
                    //console.log('begining loading ' + element.data('src'));
                },
                afterLoad: function (element) {
                    // called after an element was successfully handled
                    //console.log('after loading ' + element.data('src'));
                },
                onError: function (element) {
                    console.log('error loading ' + element.data('src'));
                },
                onFinishedAll: function () {
                    // called once all elements was handled
                    console.log('Loaded All Thumbs');
                }
            });
        }


$(document).ready(function () {

    $('body').on('click', 'a.artwork-gal', function () {
        console.log($(this));
        //onclick="focusOnMarker({{ art.id }}), markerClicked(), expandCard()"
        image_selected($(this).data('artid'));
        $('.main-image').css('height', '50%');
    });
    if (loadedart > 0) {
        image_selected(loadedart, true);
        $('.main-image').css('height', '50%');
    }
});
