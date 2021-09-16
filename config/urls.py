"""App URL routes mapping"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tracker.views import add_expense_view

urlpatterns = [
    path("user/", include("users.urls", namespace="users")),
    path("expense/", include("tracker.urls", namespace="expense")),
    path('admin/', admin.site.urls),
    path("", add_expense_view, name="add_expense"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
