"""Models for tracker app"""

from datetime import date
from django.db import models
from users.models import User

PAYMENT_METHOD = (
    ("UPI", "UPI"),
    ("CASH", "Cash"),
    ("DEB", "Debit Card"),
    ("CRE", "Credit Card"),
    ("NET", "Net Banking")
)

APPS = (
    ("CASH", "Cash"),
    ("PYTM", "Paytm"),
    ("PHPE", "PhonePe"),
    ("GPAY", "GPay"),
    ("BANK", "Bank Apps"),
    ("OTHR", "Other")
)


class Category(models.Model):
    """
    Category for each expense. Default categories will be visible to all.

    name: Name of category
    user: User who created the category
    default: If default will be visible to all users
    """
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Expense(models.Model):
    """
    Store the expenses

    user: User responsible for expense
    amount: Expense amount
    desccription: Description of expense
    date: When expense was done
    category: Category of the expense
    method: Payment method of expense
    app: Application used for the payment
    """
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=128, null=True, blank=True)
    date = models.DateField(default=date.today)
    category = models.ForeignKey(Category, db_index=True, on_delete=models.SET_NULL, null=True)
    method = models.CharField("Payment Method", choices=PAYMENT_METHOD, db_index=True, max_length=4)
    app = models.CharField("Application", choices=APPS, max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense<amount={self.amount}, category={self.category.name}, description=" \
               f"{self.description}>"
