from django import forms
from .models import Expense, Receipt

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['car', 'date', 'amount_received', 'other_expenses', 'amount', 'month']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount_received': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['name', 'phone_number', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }