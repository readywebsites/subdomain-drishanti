from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from api.views import frontend

from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),

    # Serve static assets from dist/assets
    re_path(r'^assets/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'dist', 'assets'),
    }),

    # Serve static images from dist/images
    re_path(r'^images/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'dist', 'images'),
    }),

    # React frontend catch-all
    re_path(r'^(?!admin/?$|admin/|api/).*$' , frontend),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
