"""Views for tracker app"""

import calendar
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet
from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm, ExpenseHistory
from .models import Expense, APPS, PAYMENT_METHOD


APP_DICT = dict(APPS)
METHOD_DICT = dict(PAYMENT_METHOD)


@login_required
def expense_history(request):
    """View to return expense history"""
    qs: QuerySet = Expense.objects.by_user(request.user.id)
    file_title: str = "Latest_150_Expenses"
    form = ExpenseHistory(request.GET)
    if form.is_valid():
        cd: dict = form.cleaned_data
        target: str = cd["target"]
        user_id = request.user.id
        if target == "date":
            qs = Expense.objects.filter(date=cd["date1"], user_id=user_id)
            file_title = f'For_{cd["date1"]}'
        elif target == "each_month":
            qs = Expense.objects.filter(date__month=cd["month"], user_id=user_id)
            file_title = f"Every_{calendar.month_name[cd['month']]}_Month"
        elif target == "months":
            qs = Expense.objects.last_n_months_expense(cd["p_months"], user_id)
            file_title = f"Last_{cd['p_months']}_months"
        elif target == "month":
            qs = Expense.objects.month_expense(cd["month"], cd["year"], user_id)
            file_title = f'For_{calendar.month_name[cd["month"]]}-{cd["year"]}'
        elif target == "year":
            qs = Expense.objects.year_expense(cd["year"], user_id)
            file_title = f"{cd['year']}"
        elif target == "between":
            qs = Expense.objects.filter(date__gte=cd["date1"], date__lte=cd["date2"],
                                        user__id=user_id)
            file_title = f'Between_{cd["date1"]}_{cd["date2"]}'
    qs = qs.order_by("-date", "-id").values_list(
        "date", "description", "category__name", "method", "app", "amount",
    )
    if not form.is_valid():
        qs = qs[:150]
    qs_list = []
    if qs:
        for q in qs:
            qs_list.append([
                q[0], q[1], q[2], METHOD_DICT[q[3]], APP_DICT.get(q[4], "Other"), q[5]
            ])
    file_title = f"{date.today()}_" + file_title
    return render(request, "tracker/history.html",
                  {"qs": qs_list, "file_title": file_title, "form": form})


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
    latest_10 = Expense.objects\
        .by_user(request.user.id)\
        .order_by("-date", "-id")\
        .only("amount", "date", "description")[:10]
    latest_10_total = latest_10.aggregate(Sum("amount"))

    this_month = Expense.objects.month_expense(
        today.month, today.year, request.user.id
    ).aggregate(Sum("amount"))

    last_month_date = today.replace(day=1) - timedelta(1)
    last_month = Expense.objects.month_expense(
        last_month_date.month, last_month_date.year, request.user.id
    ).aggregate(Sum("amount"))

    last_3_months = Expense.objects.last_n_months_expense(3, request.user.id)\
        .aggregate(Sum("amount"))

    this_year = Expense.objects.year_expense(today.year, request.user.id)\
        .aggregate(Sum("amount"))
    last_year = Expense.objects.year_expense(today.year - 1, request.user.id)\
        .aggregate(Sum("amount"))

    return render(request, "tracker/add.html", {
        "form": form, "latest_10": latest_10, "3_months": last_3_months["amount__sum"],
        "this_year": this_year["amount__sum"], "last_month": last_month["amount__sum"],
        "this_month": this_month["amount__sum"], "last_year": last_year["amount__sum"],
        "latest_10_sum": latest_10_total["amount__sum"]
    })
