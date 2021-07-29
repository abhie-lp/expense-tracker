"""Model manager for trackers app"""
from datetime import date, timedelta
from django.db.models import Manager, QuerySet
from utils.datetime import year_month_before, YearMonth


class ExpenseManager(Manager):
    """Manager for Expense model"""

    def by_user(self, user_id: int) -> QuerySet:
        """Return expenses for user with user_id"""
        return self.filter(user_id=user_id)

    def month_expense(self, month: int, year: int, user_id: int) -> QuerySet:
        """Return the expenses for given month and user"""
        return self.filter(date__month=month, date__year=year, user_id=user_id)

    def year_expense(self, year: int, user_id: int) -> QuerySet:
        """Return the expenses for the given year and user"""
        return self.filter(date__year=year, user_id=user_id)

    def last_n_months_expense(self, month_count: int, user_id: int) -> QuerySet:
        """Return the expenses for the last n months from today"""
        last_month = date.today().replace(day=1) - timedelta(1)
        start_date: date = date(*year_month_before(month_count), 1)
        return self.filter(user_id=user_id, date__gte=start_date, date__lte=last_month)
