from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from .models import Artwork, Artist
from mapwidgets.widgets import GooglePointFieldWidget


class SignUpForm(UserCreationForm):
	birth_date = forms.DateField(required=False, help_text='Optional. Format: YYYY-MM-DD', widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'name': 'birth_date'}))
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

class ArtworkForm(forms.ModelForm):

    class Meta:
        model = Artwork
        fields = ('title', 'artists', 'image', 'photo_credit', 'location')
        widgets = {
            'location': GooglePointFieldWidget,
        }

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ('name',)

class SettingsForm(forms.Form):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date')