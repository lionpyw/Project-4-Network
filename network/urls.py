
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.view_posts, name="allposts"),
    path("profiles/<int:person_id>", views.profile_page, name="profile"),
    path('profiles/follow/<int:person_id>', views.follow, name="follow"),
    path('following', views.follow_posts, name="follow_posts"),
    path('posted', views.post, name="post"),
    path('edit/<str:post_id>', views.edit_post, name="edit"),
    path('liked/<str:post_id>', views.like, name="like"),
    path('image/<int:person_id>', views.profile_image, name="image")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
