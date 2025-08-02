# complaint_system/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('complaints/', include('complaints.urls')),
    path('users/', include('users.urls')),
]