"""Views for tracker app"""

from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet
from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm
from .models import Expense, APPS, PAYMENT_METHOD


APP_DICT = dict(APPS)
METHOD_DICT = dict(PAYMENT_METHOD)


@login_required
def expense_history(request):
    """View to return expense history"""
    qs: QuerySet = Expense.objects.latest_expenses(request.user.id, 150)
    qs = qs.values_list(
        "date", "amount", "description", "category__name", "method", "app"
    )
    qs_list = []
    if qs:
        for q in qs:
            qs_list.append([
                q[0], q[1], q[2], q[3], METHOD_DICT[q[4]], APP_DICT.get(q[5], "Other")
            ])
    return render(request, "tracker/history.html", {"qs": qs_list})


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
    latest_10 = Expense.objects.latest_expenses(request.user.id)

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
        "this_month": this_month["amount__sum"], "last_year": last_year["amount__sum"]
    })
