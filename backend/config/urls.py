"""
TeamFlow EPMS — Root URL Configuration.

Routes:
- /admin/          → Django admin interface
- /api/v1/         → Django Ninja API (all versioned endpoints)
- /static/         → Static files (development only)
- /media/          → Media files (development only)
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
