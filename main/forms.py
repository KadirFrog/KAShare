from django import forms
from django.contrib.auth.forms import UserCreationForm

from main.models import *


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    fullname = forms.CharField(max_length=100)
    school_class = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('fullname', 'username', 'email', 'school_class')

class CustomAuthenticationForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']