"""Form for users app"""

from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    """Form to register a new user"""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = "username", "email",
