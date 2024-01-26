
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'likes', views.LikesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("", views.index, name="index"),
    path("allposts", views.view_posts, name="allposts"),
    path("profiles/<int:person_id>", views.profile_page, name="profile"),
    path('profiles/follow/<int:person_id>', views.follow, name="follow"),
    path('following', views.follow_posts, name="follow_posts"),
    path('posted', views.post, name="post"),
    path('edit/<str:post_id>', views.edit_post, name="edit"),
    path('liked/<str:post_id>', views.like, name="like"),
    path('image/<int:person_id>', views.profile_image, name="image")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
