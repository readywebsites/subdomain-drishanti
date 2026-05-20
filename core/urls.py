from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from api.views import frontend

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),

    # React frontend catch-all
    re_path(r'^(?!admin/?$|admin/|api/).*$' , frontend),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)