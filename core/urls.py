"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from api.views import frontend

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API Routes
    path('api/', include('api.urls')),

    # React Frontend Catch-All
    re_path(r'^.*$', frontend),
]

# Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)