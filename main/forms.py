from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from main.models import *


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    fullname = forms.CharField(max_length=100)
    school_class = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('fullname', 'email', 'school_class') + UserCreationForm.Meta.fields

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['classtest', 'content', 'image']

class ClassTestForm(forms.ModelForm):
    class Meta:
        model = ClassTest
        fields = ['test_name', 'test_date']
