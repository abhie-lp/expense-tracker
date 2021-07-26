"""URL route mapping for tracker app"""

from django.urls import path
from .views import expense_history

app_name = "tracker"

urlpatterns = [
    path("history/", expense_history, name="history"),
]
