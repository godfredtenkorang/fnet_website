from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'licence_number', 'phone_number', 'license_issue_date', 'licence_expiry_date', 'is_available']
        widgets = {
            'license_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'licence_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }