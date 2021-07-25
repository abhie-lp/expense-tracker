"""Views for tracker app"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm
from .models import Expense


@login_required
def add_expense_view(request):
    """View add a expense"""
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
    return render(request, "tracker/add.html", {"form": form, "previous_10": previous_10})
