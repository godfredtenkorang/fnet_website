from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['car', 'date', 'amount_received', 'drivers_commission', 'other_expenses', 'amount', 'month']