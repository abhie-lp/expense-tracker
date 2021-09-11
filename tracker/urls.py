"""URL route mapping for tracker app"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apis import analysis_api, CategoryViewSet
from .views import expense_history, analysis_view

app_name = "tracker"
router = DefaultRouter()

router.register(r"category", CategoryViewSet, basename="category")

api_urls = [
    path("analysis/", analysis_api, name="api_analysis"),
] + router.urls

urlpatterns = [
    path("history/", expense_history, name="history"),
    path("api/", include(api_urls)),
    path("analysis/", analysis_view, name="analysis"),
]
