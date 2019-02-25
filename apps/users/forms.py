from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile, Post

User = get_user_model()

class UserCreationModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'country', 'city', 'email', 'password1', 'password2', 'access_challenge']


class UserUpdateForm(UserChangeForm):
    username = forms.CharField()
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
