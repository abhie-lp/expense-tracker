"""Model manager for trackers app"""
from datetime import date, timedelta
from django.db.models import Manager, QuerySet
from utils.datetime import year_month_before, YearMonth


class ExpenseManager(Manager):
    """Manager for Expense model"""

    def latest_expenses(self, user_id: int, expenses_count: int = 10) -> QuerySet:
        """Return the latest n expenses for the user"""
        return self.filter(user_id=user_id)\
            .order_by("-date", "-id")\
            .only("amount", "date", "description")[:expenses_count]

    def month_expense(self, month: int, year: int, user_id: int) -> QuerySet:
        """Return the expenses for given month and user"""
        return self.filter(date__month=month, date__year=year, user_id=user_id)

    def year_expense(self, year: int, user_id: int) -> QuerySet:
        """Return the expenses for the given year and user"""
        return self.filter(date__year=year, user_id=user_id)

    def last_n_months_expense(self, month_count: int, user_id: int) -> QuerySet:
        """Return the expenses for the last n months from today"""
        last_month = date.today().replace(day=1) - timedelta(1)
        year_month: YearMonth = year_month_before(month_count)
        return self.filter(
            user_id=user_id, date__month__gte=year_month.month, date__year__gte=year_month.year,
            date__month__lte=last_month.month, date__year__lte=last_month.year
        )
