"""Views for users app"""

from django.shortcuts import render, redirect

from .forms import RegisterForm
from .models import User


def register_view(request):
    """View to register new user"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("users:login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})
