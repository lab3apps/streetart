from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Artwork, Artist, Profile, ArtistExpressionOfInterest, WallSpace, MuralCommission
from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.encoding import force_text
from mapwidgets.settings import MapWidgetSettings, mw_settings


def minify_if_not_debug(asset):
    """
        Transform template string `asset` by inserting '.min' if DEBUG=False
    """
    return asset.format("" if not mw_settings.MINIFED else ".min")

class MyGooglePointFieldWidget(GooglePointFieldWidget):
    template_name = "streetart/google-point-field-widget.html"
    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        if not mw_settings.MINIFED:  # pragma: no cover
            js = [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
            ]
        else:
            js = [
                "mapwidgets/js/mw_google_point_field.min.js"
            ]

        return forms.Media(js=js, css=css)
        

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(required=False, help_text='Optional. Format: DD/MM/YYYY', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'name': 'birth_date', 'type': 'date'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'type': 'password'}))

def is_int(s):
    try:
        int(str(s))
        return True
    except ValueError:
        return False

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ('submitter_description', 'submitter_name', 'submitter_email', 'image', 'location')
        widgets = {
            'location': MyGooglePointFieldWidget,
        }

class MuralCommissionForm(forms.ModelForm):
    class Meta:
        model = MuralCommission
        fields = '__all__'
        widgets = {
            'mural_location': MyGooglePointFieldWidget,
        }

class WallSpaceForm(forms.ModelForm):
    class Meta:
        model = WallSpace
        fields = '__all__'
        widgets = {
            'wall_location': MyGooglePointFieldWidget,
        }

class ArtistExpressionOfInterestForm(forms.ModelForm):
    class Meta:
        model = ArtistExpressionOfInterest
        fields = '__all__'
        
class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileSettingsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ( 'bio', 'birth_date', 'location')
