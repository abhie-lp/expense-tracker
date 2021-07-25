"""Forms for tracker app"""

from django.forms import ModelForm, ModelChoiceField, RadioSelect, ChoiceField, Textarea
from django.db.models import Q
from .models import Expense, Category, PAYMENT_METHOD, APPS


class ExpenseForm(ModelForm):
    """Expense form to add new expense"""

    class Meta:
        model = Expense
        fields = "amount", "description", "date", "category", "method", "app"
        widgets = {
            "description": Textarea()
        }

    def __init__(self, request, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields["category"] = ModelChoiceField(
            Category.objects.filter(Q(default=True) | Q(user=request.user)).only("id", "name"),
            widget=RadioSelect(attrs={"autocomplete": "off", "class": "btn-check"})
        )
        self.fields["method"] = ChoiceField(choices=PAYMENT_METHOD, widget=RadioSelect(attrs={
            "autocomplete": "off", "class": "btn-check"
        }))
        self.fields["app"] = ChoiceField(choices=APPS, widget=RadioSelect(attrs={
            "autocomplete": "off", "class": "btn-check"
        }), required=False)
        self.fields["date"].required = False
        self.fields["app"].label = "Application"
