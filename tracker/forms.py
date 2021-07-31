"""Forms for tracker app"""

from datetime import date
from django.forms import Form, ModelForm, ModelChoiceField, RadioSelect, TypedChoiceField, \
    DateField, IntegerField, DateInput, CharField, Textarea, ValidationError, ChoiceField
from django.db.models import Q
from .models import Expense, Category, PAYMENT_METHOD, APPS

MONTH = tuple((ind, mon) for ind, mon in enumerate((
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
), 1))


class ExpenseHistory(Form):
    """Form to filter expenses of a user"""
    p_months = IntegerField(min_value=1, max_value=36, initial=3, required=False)
    month = TypedChoiceField(choices=MONTH, required=False, coerce=int)
    year = TypedChoiceField(choices=tuple((y, y) for y in range(date.today().year, 1999, -1)),
                            required=False, coerce=int)
    date1 = DateField(widget=DateInput(
        attrs={"type": "date", "class": "form-control", "required": True}
    ), required=False)
    date2 = DateField(widget=DateInput(
        attrs={"type": "date", "class": "form-control", "required": True}
    ), required=False)
    target = CharField(max_length="10")

    def __init__(self, *args, **kwargs):
        super(ExpenseHistory, self).__init__(*args, **kwargs)
        self.fields["p_months"].widget.attrs = {"class": "form-control", "required": True,
                                                "min": 1, "max": 37}
        self.fields["month"].widget.attrs = {"class": "form-control", "required": True}
        self.fields["year"].widget.attrs = {"class": "form-control", "required": True}

    def clean_target(self):
        """Validate other inputs based on target"""
        cd = self.cleaned_data
        target = cd["target"]
        if target == "months":
            if not 0 < cd["p_months"] <= 36:
                raise ValidationError("Number of months should be between 1 and 36")
        elif target == "month" or target == "each_month":
            if not 1 <= cd["month"] <= 12 and \
                    not 2000 <= cd["year"] <= date.today().year:
                raise ValidationError("Enter month between Jan and Dec and Year between 2000 and "
                                      "current year")
        elif target == "year":
            if not 2000 <= cd["year"] <= date.today().year:
                raise ValidationError("Enter year between 2000 and current year")
        elif target == "between":
            start, end = cd["date1"], cd["date2"]
            if not start < end:
                raise ValidationError("Start date cannot be greater than end date")
        elif target == "date":
            if not cd["date1"]:
                raise ValidationError("Enter valid date and in YYYY-MM-DD format")
        else:
            raise ValidationError("Wrong data description.")
        return target


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
