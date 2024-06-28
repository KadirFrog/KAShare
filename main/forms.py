from django import forms
from django.contrib.auth.forms import UserCreationForm

from main.models import *


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    fullname = forms.CharField(max_length=100)
    school_class = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    class Meta:
        model = CustomUser
        fields = ('fullname', 'username', 'email', 'password', 'school_class')

class CustomAuthenticationForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']