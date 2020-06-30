from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from register_from_file.views import upload_file, ViewUploadFile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('upload_file/', upload_file, name='upload_file'),
    path('view_file/', ViewUploadFile, name='view_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
