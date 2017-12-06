
function get_artist_bio(art) {
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
    var bio_html = '';
    if (art.title != "") {
        bio_html += '<p class="card-title">\
            <span class="artwork-title">'+art.title+'</span>\
        </p>';
    }
    if (artists_text != "") {
        bio_html += '<p class="card-artists">\
            <span class="artwork-artists">'+artists_text+'</span>\
        </p>';
    }
    if (art.description != "") {
        bio_html += '<p class="card-description">\
            <span class="artwork-description">'+art.description+'</span>\
        </p>';
    }

    for(var key in art) {
        if (art[key] != 'None' && art[key] != '') {
            if (key == 'commission_date' || key == 'decommission_date') {
                bio_html += '<p class="card-generated">\
                    <span class="value-title">'+key.replace('_', ' ')+': </span>\
                    <span class="artwork-'+key+'">'+art[key]+'</span>\
                </p>';
            } else if (key == 'link') {
                bio_html += '<p class="card-generated">\
                    <span class="value-title">'+key.replace('_', ' ')+': </span>\
                    <span class="artwork-'+key+'"><a href="'+art[key]+'">'+art[key]+'</a></span>\
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
    $('.fullscreen-link').attr('href', art.imageUrl);
}

function load_child_tools(art, index) {
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

}

function image_selected(index) {
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        var marker = markers[index];
        var point = new google.maps.LatLng(art.lat, art.lng);

        getNearestArtworks(index);
        // Image Loading
        load_artwork_main_image(art);
        get_artist_bio(art);
        load_child_tools(art, index);
        
        map.panTo(point);
        map.setZoom(17);
        toggleBounce(marker);
        loadCommentSection(index);
        loadAltImages(index);
        history.replaceState({}, null, '/artwork/'+index);
        full_card_view();
    }
}

function focusOnMarker(index) {
    //image_selected(index);

    if (arrayHasOwnIndex(artworks, index)) {
        full_card_view();
        var art = artworks[index];
        var marker = markers[index];
        getNearestArtworks(index);
        $("#left-panel").scrollTop(0);

        //closeMarkers();
        //marker['infowindow'].open(map, marker);
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

        $("#card-content").html('');
        var overlay_title = '';
        if (artists_text !== "") {
            overlay_title = artists_text;
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
        $('.fullscreen-link').attr('href', art.imageUrl);
        if(art.hasLiked === 'True') {
            $('#like-icon-unfilled').hide();
            $('#like-icon-filled').show();
        } else {
            $('#like-icon-unfilled').show();
            $('#like-icon-filled').hide();
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
        toggleBounce(marker);
        loadCommentSection(index);
        loadAltImages(index);
        history.replaceState({}, null, '/artwork/'+index);
        //setTimeout(function(){ expandCard(); }, 10);
        
    }
}

function panToPointIfNeeded(index) {
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        var point = new google.maps.LatLng(art.lat, art.lng);
        map.panTo(point);
        map.setZoom(18);
    }
}

$('#show_on_map').click(function(e) {
    $('.left-panel').addClass('mobile-hide');
    $('.right-panel').removeClass('mobile-hide');
    showRightPanel();
    google.maps.event.trigger(map, "resize");
    var marker_index = $(this).data('index');
    if (arrayHasOwnIndex(artworks, marker_index)) {
        var art = artworks[marker_index];
        var point = new google.maps.LatLng(art.lat, art.lng);
        var thisMarker = markers[marker_index];
        toggleBounce(thisMarker);
        map.setZoom(18);
        map.panTo(point);
    }
});

function getNearestArtworks(index) {
    if (csrftoken !== null || csrftoken !== '' || typeof(csrftoken) !== 'undefined') {
        $.ajax({
            async:'true',
            url: '/nearby/' + index + '/',
            data: {'csrfmiddlewaretoken': csrftoken},
            type: 'GET',
            success: function(response) {
                RenderNearestArtworks(response,index);
            },
            failure: function(error) {
                console.error(error);
            }
        });
    }
}

function RenderNearestArtworks(response,_index){
    res =  jQuery.parseJSON( response );
    $("#nearest-artworks-holder").html("");
    var no_of_nearest = res.length-1;
    if(no_of_nearest < 1){
        $("#nearest-artworks-header").hide();
    }
    var elements_in_row = 4;
    var height_of_row =109;    //px
    var no_of_rows = Math.floor(no_of_nearest/elements_in_row);
    if(no_of_nearest%elements_in_row>0)
    {
    no_of_rows++;
    }

    //$("#nearest-artworks-holder").height( no_of_rows * height_of_row);
    $.each(res, function (index,obj)
    {
        if(_index!=obj.pk)
        {
        var imagetag ;
        if(obj.fields.cropped_image=="")
        {
        imagetag = '<img class="lazy thumbnail-image" src="/media/'+obj.fields.image+'" >';
        }else
        {
        imagetag = '<img class="lazy thumbnail-image" src="/media/'+obj.fields.cropped_image+'" >';
        }

        var view ='<div id="artbox-'+obj.pk+'" class="gallery-item col-xs-6 col-sm-3 col-md-3">'+
                    '<div class="dummy"></div>'+
                    '<a class="img-link" onclick="focusOnMarker('+obj.pk+')">'+ imagetag+
                    '</a>'+
                '</div>';
        $("#nearest-artworks-holder").append(view);
        }
    });
}


/* Loads the comment section into html using ajax request with the index on clicked artwork */
function loadCommentSection(index) {
    if (arrayHasOwnIndex(artworks, index)) {
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
    if (arrayHasOwnIndex(artworks, index)) {
        var art = artworks[index];
        if(art.altImages.length >= 1) {
            $('#images-card-holder').empty();
            $('#images-card-holder').append('<div id="alt-images-card" class="card"></div>');
            for(var key in art.altImages) {
                if(art.altImagesCredit[key] != 'None' && art.altImagesCredit[key]!=''){
                    $('#alt-images-card').append('<a id="alt-image" href="' +  art.altImages[key] + '" data-lightbox="lightbox" class="col-xs-3"  data-title="Photo Credit: '+ art.altImagesCredit[key] +'"><img class="img-responsive" src="' + art.altImages[key] + '"></a>');
                }
                else{
                    $('#alt-images-card').append('<a id="alt-image" href="' +  art.altImages[key] + '" data-lightbox="lightbox" class="col-xs-3"><img class="img-responsive" src="' + art.altImages[key] + '"></a>');
                }
            }
        } else {
            $('#images-card-holder').empty();
        }
    }
}

$( document ).ready(function() { //TODO: make a document ready as well - just need this for the map stuff.

    $('body').on('click', 'a.artwork-gal', function() {
        focusOnMarker($(this).data('artid'));
        panToPointIfNeeded($(this).data('artid'));
    });
    if (loadedart > 0) {
        focusOnMarker(loadedart);
    } else {
        var hash = location.hash.replace('#', '');
        if ($(window).width() <= 991) {
            if (hash === 'gallery') {
                showGalleryMobile();
            } else if (hash === 'map') {
                showMapMobile();
            }
        } else {
            if (hash === 'gallery') {
                perform_right_toggle();
            } else if (hash === 'map') {
                perform_left_toggle();
            }
        }
    }
});
window.onload = function() { //TODO: make a document ready as well - just need this for the map stuff.
    if (loadedart > 0) {
        panToPointIfNeeded(loadedart);
    } 
};