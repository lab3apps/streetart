from django.core import serializers
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.gis import geos
from django.contrib.gis.measure import D
from social_django.models import UserSocialAuth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import SignUpForm, ArtworkForm, MuralCommissionForm, WallSpaceForm, ArtistExpressionOfInterestForm, UserSettingsForm, ProfileSettingsForm
from .serializers import ArtworkSerializer, ArtistSerializer, RouteSerializer
from .models import Artwork, Artist, Status, Route, Section, Logo
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings as site_settings

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST

def home(request, **kwargs):
    artwork = Artwork.objects.filter(validated=True).order_by('pk')
    section = Section.objects.order_by('order')
    if request.user.is_authenticated():
        for art in artwork:
            art.has_liked = art.likes.filter(id=request.user.id).exists()
            art.has_checkedin = art.checkins.filter(id=request.user.id).exists()
    else:
        for art in artwork:
            art.has_liked = False
            art.has_checkedin = False

    if ('pk' in kwargs):
        try:
            Artwork.objects.get(pk=kwargs.get('pk'))
        except Artwork.DoesNotExist:
            ##return Response(status=status.HTTP_404_NOT_FOUND)
            messages.error(request, 'This artwork does not exist.')
            return redirect('/')
        return render(request, 'streetart/home.html', {'artworks': artwork, 'sections': section, 'loadedart': kwargs.get('pk')})
    else:
        return render(request, 'streetart/home.html', {'artworks': artwork, 'sections': section})


@login_required
@transaction.atomic
def settings(request):
    user = request.user

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    if request.method == 'POST':
        userForm = UserSettingsForm(request.POST, instance=request.user)
        profileForm = ProfileSettingsForm(request.POST, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, 'Your profile was successfully updated')
            return redirect('/settings')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        userForm = UserSettingsForm(instance=request.user)
        profileForm = ProfileSettingsForm(instance=request.user.profile)

    return render(request, 'registration/settings.html', {
        'settingsForm': userForm,
        'profileForm': profileForm,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def add_new(request):
    '''
    Handles displaying, validating and saving a artwork and related
    model artist
    '''
    artworkForm = ArtworkForm()
    muralCommissionForm = MuralCommissionForm()
    wallSpaceForm = WallSpaceForm()
    artistExpressionOfInterestForm = ArtistExpressionOfInterestForm()

    if request.method == "POST":
        if 'new_artwork' in request.POST:
            artworkForm = ArtworkForm(request.POST, request.FILES)
            if artworkForm.is_valid():
                # do something with the form data here
                artwork = artworkForm.save(commit=False)
                artwork.author = request.user
                artwork.published_date = timezone.now()
                artwork.save()
                artworkAdminURL = 'christchurchstreetart.org.nz/admin/streetart/artwork/'
                send_mail('New Artwork', 'A art work has been subimitted by a user, find it here: '+artworkAdminURL+str(artwork.id), site_settings.EMAIL_FROM, [site_settings.MODERATOR_EMAIL])
                return redirect('/thanks', pk=artwork.pk)
            else:
                if 'location' in artworkForm.errors.as_data():
                    messages.error(request, 'Please choose a location.')
                else:
                    messages.error(request, 'There was an unexpected error when submitting. Please check your entries and try again.')
        elif 'new_muralcommission' in request.POST:
            muralCommissionForm = MuralCommissionForm(request.POST, request.FILES)
            if muralCommissionForm.is_valid():
                # do something with the form data here
                muralCommission = muralCommissionForm.save(commit=False)
                muralCommission.author = request.user
                muralCommission.published_date = timezone.now()
                muralCommission.save()
                muralAdminURL = 'christchurchstreetart.org.nz/admin/streetart/muralcommission/'
                send_mail('New Mural Comission', 'A new mural commission has been subimitted by a user, find it here: '+muralAdminURL+str(muralCommission.id), site_settings.EMAIL_FROM, [site_settings.MODERATOR_EMAIL])
                return redirect('/thanks')
            else:
                if 'mural_location' in muralCommissionForm.errors.as_data():
                    messages.error(request, 'Please choose a location.')
                else:
                    messages.error(request, 'There was an unexpected error when submitting. Please check your entries and try again.')
                
        elif 'new_wallspace' in request.POST:
            wallSpaceForm = WallSpaceForm(request.POST, request.FILES)
            if wallSpaceForm.is_valid():
                # do something with the form data here
                wallSpace = wallSpaceForm.save(commit=False)
                wallSpace.author = request.user
                wallSpace.published_date = timezone.now()
                wallSpace.save()
                wallspaceAdminURL = 'christchurchstreetart.org.nz/admin/streetart/wallspace/'
                send_mail('New Wall Space', 'A new wall space has been subimitted by a user, find it here: '+wallspaceAdminURL+str(wallSpace.id), site_settings.EMAIL_FROM, [site_settings.MODERATOR_EMAIL])
                return redirect('/thanks')
            else:
                if 'wall_location' in wallSpaceForm.errors.as_data():
                    messages.error(request, 'Please choose a location.')
                else:
                    messages.error(request, 'There was an unexpected error when submitting. Please check your entries and try again.')
        elif 'new_artistexpressionofinterest' in request.POST:
            artistExpressionOfInterestForm = ArtistExpressionOfInterestForm(request.POST)
            if artistExpressionOfInterestForm.is_valid():
                # do something with the form data here
                artistExpressionOfInterest = artistExpressionOfInterestForm.save(commit=False)
                artistExpressionOfInterest.author = request.user
                artistExpressionOfInterest.published_date = timezone.now()
                artistExpressionOfInterest.save()
                artistEOIAdminURL = 'christchurchstreetart.org.nz/admin/streetart/artistexpressionofinterest/'
                send_mail('New Artist EOI', 'A new artist expression of interest has been subimitted by a user, find it here: '+artistEOIAdminURL+str(artistExpressionOfInterest.id), site_settings.EMAIL_FROM, [site_settings.MODERATOR_EMAIL])
                return redirect('/thanks')

    return render(request, "streetart/add_new_form.html", {'artworkForm': artworkForm, 'muralCommissionForm': muralCommissionForm, 'wallSpaceForm': wallSpaceForm, 'artistExpressionOfInterestForm': artistExpressionOfInterestForm, 'url_name': request.resolver_match.url_name})

# API Functions

@api_view(['GET'])
def artwork_list(request):
    """
    List all artworks.
    """
    if request.method == 'GET':
        artworks = Artwork.objects.all()
        serializer = ArtworkSerializer(artworks, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def artwork_detail(request, pk):
    """
    Retrieve, update or delete an artwork instance.
    """
    try:
        artwork = Artwork.objects.get(pk=pk)
    except Artwork.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtworkSerializer(artwork)
        return Response(serializer.data)

@api_view(['GET'])
def artist_list(request):
    """
    List all artists.
    """
    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def artist_detail(request, pk):
    """
    Retrieve, update or delete an artist instance.
    """
    try:
        artist = Artist.objects.get(pk=pk)
    except Artist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

@api_view(['GET'])
def route_list(request):
    """
    List all routes.
    """
    if request.method == 'GET':
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def route_detail(request, pk):
    """
    Retrieve, update or delete a route instance.
    """
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RouteSerializer(route)
        return Response(serializer.data)

def closest_artwork(request, index):
    artworkObject = Artwork.objects.get(pk=index)
    artwork = get_closest_artworks(artworkObject.location.y, artworkObject.location.x)
    response = serializers.serialize("json", artwork)
    return render(request, 'streetart/ordered_artwork_list.html', {'artworks': artwork})

def get_closest_artworks(lat, long):
    point = geos.fromstr("POINT(%s %s)" % (long, lat))
    artworks = Artwork.objects.filter(location__distance_lte=(point, D(km=10))).distance(point).order_by('distance')
    return artworks

def image_selected(request, index):
    return render(request, 'streetart/card_detail_body.html', {'art': Artwork.objects.get(pk=index)})

@login_required
@require_POST
def like(request, key):
    if request.method == 'POST':
        user = request.user
        artwork = get_object_or_404(Artwork, pk=key)

        if artwork.likes.filter(id=user.id).exists():
            # user has already liked this artwork
            # remove like/user
            artwork.likes.remove(user)
            message = 'unliked'
        else:
            # add a new like for a artwork
            artwork.likes.add(user)
            message = 'liked'

    ctx = {'likes_count': artwork.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@require_POST
def checkIn(request, key):
    if request.method == 'POST':
        user = request.user
        artwork = get_object_or_404(Artwork, pk=key)

        if artwork.checkins.filter(id=user.id).exists():
            # user has already liked this artwork
            # remove like/user
            artwork.checkins.remove(user)
            message = 'checkedout'
        else:
            # add a new like for a artwork
            artwork.checkins.add(user)
            message = 'checkedin'

    ctx = {'checkins_count': artwork.total_checkins, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')

def thanks(request):
    return render(request, 'streetart/thank_you.html')

def logos(request):
    logos = Logo.objects.all()
    return render(request, 'streetart/logos.html', {'logos': logos})

def post_comment(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        artwork = request.POST.get('artwork')
        text = request.POST.get('text')
        response_data = {
            'author' : author,
            'text' : text,
            'artwork' : artwork
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

