"""App URL routes mapping"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("user/", include("users.urls", namespace="users")),
    path('admin/', admin.site.urls),
]
