from django.conf.urls.static import static
from django.urls import path

from KAShare import settings
from main import views

urlpatterns = [path("post", views.post, name="post"),
               path("", views.profile, name="profile"),
               path("accounts/login/?next=/", views.login_view, name="login"),
               path("sign_up", views.signup_view, name="sign_up"),
               path("login", views.login_view, name="login"),
               path("logout", views.logout_view, name="logout"),
               path("recent_posts", views.recent_posts, name="recent_posts"),
               path("post/<int:post_id>", views.post_detail, name="post_detail"),
               path("post/<int:post_id>/like", views.like_post, name="like_post"),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
