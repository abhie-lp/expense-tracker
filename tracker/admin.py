"""Models to show in Django admin"""

from django.contrib import admin

from .models import Expense, Category


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Expense model data for admin"""
    list_display = "id", "user", "amount", "date", "category", "method", "app",
    list_filter = "date", "method", "app",


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category model data for admin"""
    list_display = "name", "user", "default", "created_at",
    list_filter = "default", "created_at", "name",
