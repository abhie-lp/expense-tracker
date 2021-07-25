"""Views for tracker app"""

from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from utils.datetime import year_month_before, YearMonth
from .forms import ExpenseForm
from .models import Expense


@login_required
def add_expense_view(request):
    """View add a expense"""
    today = date.today()
    if request.method == "POST":
        form = ExpenseForm(request, request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user.id
            expense.save()
            return redirect("add_expense")
    else:
        form = ExpenseForm(request)
    previous_10 = Expense.objects\
        .filter(user_id=request.user.id) \
        .order_by("-date", "-id") \
        .only("amount", "date", "description")[:10]

    this_month = Expense.objects.filter(
        user_id=request.user.id, date__month=today.month, date__year=today.year
    ).aggregate(Sum("amount"))

    last_month_date = today.replace(day=1) - timedelta(1)
    last_month = Expense.objects.filter(
        user_id=request.user.id, date__month=last_month_date.month, date__year=last_month_date.year
    ).aggregate(Sum("amount"))

    year_month: YearMonth = year_month_before(3)
    last_3_months = Expense.objects.filter(
        user_id=request.user.id, date__month__gte=year_month.month, date__year__gte=year_month.year,
        date__month__lte=last_month_date.month, date__year__lte=last_month_date.year
    ).aggregate(Sum("amount"))

    this_year = Expense.objects.filter(
        user_id=request.user.id, date__year=today.year
    ).aggregate(Sum("amount"))
    last_year = Expense.objects.filter(
        user_id=request.user.id, date__year=today.year - 1
    ).aggregate(Sum("amount"))
    return render(request, "tracker/add.html", {
        "form": form, "previous_10": previous_10, "3_months": last_3_months["amount__sum"],
        "this_year": this_year["amount__sum"], "last_month": last_month["amount__sum"],
        "this_month": this_month["amount__sum"], "last_year": last_year["amount__sum"]
    })
