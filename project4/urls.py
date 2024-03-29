"""project4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from core.views import TokenCookieDeleteView, TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("network.urls")),
    path("", include("core.urls")),
    path('__debug__/', include(debug_toolbar.urls)), path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/delete/', TokenCookieDeleteView.as_view(), name='token_delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    # urlpatterns +=  path("__debug__/", include(debug_toolbar.urls))
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
