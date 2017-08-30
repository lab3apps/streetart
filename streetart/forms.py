from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Artwork, Artist, Profile, ArtistExpressionOfInterest, WallSpace, MuralCommission
from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from django_select2.forms import (
    ModelSelect2TagWidget,
)
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

class ArtistSelect2TagWidget(ModelSelect2TagWidget):
    queryset = Artist.objects.all()
    search_fields = [
        'name__icontains',
    ]

    def value_from_datadict(self, data, files, name):
        values = super(ArtistSelect2TagWidget, self).value_from_datadict(data, files, name)
        qs = self.queryset.filter(**{'pk__in': [l for l in values if is_int(l)]})
        names = [k.name for k in self.queryset.filter(**{'name__in': values})]
        pks = set(force_text(getattr(o, 'pk')) for o in qs)
        cleaned_values = []
        for val in values:
            if force_text(val) not in pks and force_text(val) not in names:
                val = self.queryset.create(name=val).pk
            cleaned_values.append(val)
        return cleaned_values

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
        fields = ('title', 'description', 'contact')

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
        fields = ('title', 'description', 'contact')

class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileSettingsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ( 'bio', 'birth_date', 'location')
