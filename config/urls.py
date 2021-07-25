"""App URL routes mapping"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tracker.views import add_expense_view

urlpatterns = [
    path("user/", include("users.urls", namespace="users")),
    path('admin/', admin.site.urls),
    path("", add_expense_view, name="add_expense"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
