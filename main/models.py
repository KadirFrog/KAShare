from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    school_class = models.CharField(max_length=100)
    account_balance = models.FloatField(default=0.0)
    account_type = models.CharField(max_length=100, default="Student")
    REQUIRED_FIELDS = ['fullname', 'email', 'school_class']
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = True
    is_active = True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

CustomUser: CustomUser = get_user_model()


class ClassTest(models.Model):
    test_name = models.CharField(max_length=100)
    test_date = models.DateField()
    related_class = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='classtests')

    def __str__(self):
        return self.test_name

class Post(models.Model):
    title = models.CharField(max_length=255, default="")
    classtest = models.ForeignKey(ClassTest, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='likes', blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    def like_post(self, user):
        if self.user_has_liked(user):
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists()

class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
