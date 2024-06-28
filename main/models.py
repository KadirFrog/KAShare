from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    school_class = models.CharField(max_length=100)
    account_balance = models.FloatField(default=0.0)
    account_type = models.CharField(max_length=100, default="Student")
    REQUIRED_FIELDS = ['fullname', 'email', 'school_class']
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = True
    is_active = True

CustomUser: CustomUser = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='likes', blank=True)
