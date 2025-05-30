from django import forms
from .models import Customer, LoadCarImagesForCustomer, MileageRecord, FuelRecord, Expense, OilChange, Notification
from my_site.models import Driver


class SMSForm(forms.Form):
    RECIPIENT_TYPE_CHOICES = [
        ('customers', 'Customers'),
        ('drivers', 'Drivers'),
    ]
    
    recipient_type = forms.ChoiceField(
        choices=RECIPIENT_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )
    
    phone_numbers = forms.MultipleChoiceField(
        choices=[],  # Will populate dynamically
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message here'}),
        max_length=500,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate phone_numbers dynamically
        customers = Customer.objects.values_list('phone_number', 'name')
        drivers = Driver.objects.values_list('phone_number', 'first_name')
        all_numbers = [(num, f"{name} ({num})") for num, name in list(customers) + list(drivers)]
        self.fields['phone_numbers'].choices = all_numbers
        


class LoadImageForCustomerForm(forms.ModelForm):
    class Meta:
        model = LoadCarImagesForCustomer
        fields = ['customer', 'image']
        
        
        

class MileageRecordForm(forms.ModelForm):
    class Meta:
        model = MileageRecord
        fields = ['driver', 'vehicle', 'date', 'start_mileage', 'end_mileage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class UpdateMileageRecordForm(forms.ModelForm):
    class Meta:
        model = MileageRecord
        fields = ['end_mileage']
        
        
class FuelRecordForm(forms.ModelForm):
    class Meta:
        model = FuelRecord
        fields = ['vehicle', 'date', 'liters', 'amount', 'station_name', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'type', 'amount', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }
        
class OilChangeForm(forms.ModelForm):
    class Meta:
        model = OilChange
        fields = ['vehicle', 'date', 'mileage', 'cost']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'notification_type']