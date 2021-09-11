"""APIs for tracker app"""

from datetime import date

from django.db.models import Sum

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from .models import Expense
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    """Category ViewSet to manage user categories"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        """All categories for the current user"""
        return self.request.user.category_set.all()

    def perform_create(self, serializer: CategorySerializer):
        """Override to set logged-in user for category user field"""
        serializer.save(user_id=self.request.user.id)


@api_view()
def analysis_api(request):
    """API for analysis data for the user"""
    today = date.today()
    user_id = request.user.id
    months_day = Expense.objects.by_user(user_id).filter(date__year=today.year)\
        .values("date__month", "date__day", "category__name")\
        .annotate(total=Sum("amount"))
    year_month = Expense.objects.by_user(user_id)\
        .filter(date__year__gte=date.today().year-4, date__year__lte=date.today().year-1) \
        .values("date__year", "date__month", "category__name")\
        .annotate(total=Sum("amount"))
    return Response({"month_day_category": months_day,
                     "year_month_category": year_month})
