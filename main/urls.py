from django.urls import path

from main import views

urlpatterns = [path("post", views.post, name="post"),
                path("", views.profile, name="profile"),
                path("accounts/login", views.login_view, name="login"),
                path("sign_up", views.signup_view, name="sign_up"),
                path("login", views.login_view, name="login"),
               ]
