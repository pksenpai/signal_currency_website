from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('signal/', include('apps.signals.urls')),
    path('profile/', include('apps.users.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')), # The CKEditor path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
