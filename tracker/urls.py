"""URL route mapping for tracker app"""

from django.urls import path, include
from .apis import analysis_api
from .views import expense_history, analysis_view

app_name = "tracker"

api_urls = [
    path("analysis/", analysis_api, name="api_analysis"),
]

urlpatterns = [
    path("history/", expense_history, name="history"),
    path("api/", include(api_urls)),
    path("analysis/", analysis_view, name="analysis"),
]
