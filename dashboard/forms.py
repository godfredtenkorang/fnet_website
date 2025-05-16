from django import forms
from .models import Customer, LoadCarImagesForCustomer
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
        
        
