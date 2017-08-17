from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from .models import Artwork


class SignUpForm(UserCreationForm):
	birth_date = forms.DateField(required=False, help_text='Optional. Format: YYYY-MM-DD')
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

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
        fields = ('name', 'artist', 'image', 'location',)