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
from .forms import SignUpForm, ArtworkForm, UserSettingsForm, ProfileSettingsForm
from .serializers import ArtworkSerializer, ArtistSerializer
from .models import Artwork, Artist, Status
from django.db import transaction

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'streetart/home.html', {'artworks': Artwork.objects.all().order_by('pk')})
    #artworks = Artwork.objects.all().order_by('pk')
    #response = serializers.serialize("json", artworks)
    #return render(request, 'streetart/home.html', {'artworksJson': json_artworks, 'artworks': artworks})

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

def new_artwork(request):
    '''
    Handles displaying, validating and saving a artwork and related
    model artist
    '''
    artworkForm = ArtworkForm()
    if request.method == "POST":
        artworkForm = ArtworkForm(request.POST, request.FILES)
        if artworkForm.is_valid():
            # do something with the form data here
            artwork = artworkForm.save(commit=False)
            artwork.author = request.user
            artwork.published_date = timezone.now()
            artwork.save()
            artworkForm.save_m2m()
            return redirect('/', pk=artwork.pk)
    return render(request, "streetart/artwork_form.html", {'artworkForm': artworkForm,})


class ArtworkCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

class ArtistCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

def closest_artwork(request, index):
    artworkObject = Artwork.objects.get(pk=index)
    artwork = get_closest_artworks(artworkObject.location.y, artworkObject.location.x)
    response = serializers.serialize("json", artwork)
    return HttpResponse(response, content_type='application/json')

def get_closest_artworks(lat, long):
    point = geos.fromstr("POINT(%s %s)" % (long, lat))
    artworks = Artwork.objects.filter(location__distance_lte=(point, D(km=10))).distance(point).order_by('distance')
    return artworks

def image_selected(request, index):
    return render(request, 'streetart/card_detail_body.html', {'art': Artwork.objects.get(pk=index)})

@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        artwork = get_object_or_404(Artwork, slug=slug)

        if artwork.likes.filter(id=user.id).exists():
            # user has already liked this artwork
            # remove like/user
            artwork.likes.remove(user)
            message = 'You unliked this'
        else:
            # add a new like for a artwork
            artwork.likes.add(user)
            message = 'You liked this'

    ctx = {'likes_count': artwork.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@require_POST
def checkIn(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        artwork = get_object_or_404(Artwork, slug=slug)

        if artwork.checkins.filter(id=user.id).exists():
            # user has already liked this artwork
            # remove like/user
            artwork.checkins.remove(user)
            message = 'You have checked out'
        else:
            # add a new like for a artwork
            artwork.checkins.add(user)
            message = 'You have checked in'

    ctx = {'checkins_count': artwork.total_checkins, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')

