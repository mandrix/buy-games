"""
URL configuration for games project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from games.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path("api/", include("product.urls")),
    path("api/administration/", include("administration.urls")),
    path("", include("ui.urls")),
]

admin_site.site_header = "Ready Games Admin"
admin_site.site_title = "Ready Games Admin"
admin_site.index_title = "Welcome to Ready Games Admin"

# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL_SERVE_STATIC_FILES:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.LOCAL_SERVE_MEDIA_FILES:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
