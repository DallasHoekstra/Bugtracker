from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

# Wanted to add the email address to the registration form
class UserRegisterForm(UserCreationForm):
    # Required = true by default
    email = forms.EmailField()

    # nested namespace for configurations and keeps configurations in one place
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Wanted to be able to update user information 
class UserUpdateForm(forms.ModelForm):
    # Required = true by default
    email = forms.EmailField()

    # nested namespace for configurations and keeps configurations in one place
    class Meta: 
        model = User
        fields = ['username', 'email']

# Wanted to be able to update profile information
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']