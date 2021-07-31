"""Model manager for trackers app"""
from collections import namedtuple
from datetime import date, timedelta

from django.db.models import Manager, QuerySet, Q, Sum

from utils.datetime import year_month_before

ThisAndLast = namedtuple("ThisAndLast", ("this", "last"))


class ExpenseManager(Manager):
    """Manager for Expense model"""

    @staticmethod
    def last_month() -> date:
        """Return the last month"""
        return date.today().replace(day=1) - timedelta(1)

    def by_user(self, user_id: int) -> QuerySet:
        """Return expenses for user with user_id"""
        return self.filter(user_id=user_id)

    def month_expense(self, month: int, year: int, user_id: int) -> QuerySet:
        """Return the expenses for given month and user"""
        return self.by_user(user_id).filter(date__month=month, date__year=year)

    def year_expense(self, year: int, user_id: int) -> QuerySet:
        """Return the expenses for the given year and user"""
        return self.by_user(user_id).filter(date__year=year)

    def last_n_months_expense(self, month_count: int, user_id: int) -> QuerySet:
        """Return the expenses for the last n months from today"""
        last_month = self.last_month()
        start_date: date = date(*year_month_before(month_count), 1)
        return self.by_user(user_id).filter(date__gte=start_date, date__lte=last_month)

    def total_of_this_and_last_month(self, user_id: int) -> ThisAndLast:
        """Return dict with total expense in last and previous months"""
        today, last_mon_date = date.today(), self.last_month()

        # Result if received in ascending order of month irrespective of year
        result = self.by_user(user_id).filter(
            Q(date__month=today.month, date__year=today.year) |
            Q(date__month=last_mon_date.month, date__year=last_mon_date.year)
        ).values("date__month").annotate(Sum("amount"))
        if not result:
            return ThisAndLast(None, None)

        # Maybe current or previous month's expense not present hence only one result
        if len(result) == 1:
            if result[0]["date__month"] == today.month:
                return ThisAndLast(this=result[0]["amount__sum"], last=None)
            return ThisAndLast(this=None, last=result[0]["amount__sum"])

        # In case if current month is 1 then previous month will be 12 and present at 2nd index
        if result[0]["date__month"] == today.month:
            return ThisAndLast(this=result[0]["amount__sum"], last=result[1]["amount__sum"])
        return ThisAndLast(this=result[1]["amount__sum"], last=result[0]["amount__sum"])

    def total_of_this_and_last_year(self, user_id: int) -> ThisAndLast:
        """Return dict with total expense in last and previous year"""
        today = date.today()
        # Result if received in ascending order of month irrespective of year
        result = self.by_user(user_id).filter(
            Q(date__year=today.year) | Q(date__year=today.year - 1)
        ).values("date__year").annotate(Sum("amount"))
        if not result:
            return ThisAndLast(None, None)

        # In case their is no expense for last or this year
        elif len(result) == 1:
            if result[0]["date__year"] == today.year:
                return ThisAndLast(result[0]["amount__sum"], None)
            return ThisAndLast(None, result[0]["amount__sum"])
        return ThisAndLast(result[1]["amount__sum"], result[0]["amount__sum"])
