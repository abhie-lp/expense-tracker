"""Utility functions  regarding date and time"""

from datetime import date
from collections import namedtuple

YearMonth = namedtuple("YearMonth", ("year", "month"))


def year_month_before(months: int) -> YearMonth:
    """Get year and before n months"""
    today = date.today()
    month = today.month - months
    if month <= 0:
        # Subtract 1 from current year and then subtract
        # then divident from absolute value of months divided by 12
        year = today.year - 1 - abs(month) // 12
        # Since we are going backwards abs(month) % 12 returns month value from December
        # 12 + -(abs(month) % 12) Adding 12 to the negative of abs(month) gives the value from Jan
        month = 12 + -(abs(month) % 12)
    else:
        year = today.year
    return YearMonth(year, month)
