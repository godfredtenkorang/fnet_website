from django import forms
from .models import Appointment, Payment, Rental
from my_site.models import Driver


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['car', 'customer_name', 'customer_phone', 'schedule_date', 'pick_up_time', 'drop_off_time', 'pick_up_location', 'drop_off_location', 'gps_address', 'driver', 'status', 'commission_rate', 'purpose', 'total_price']
        widgets = {
            'schedule_date': forms.DateInput(attrs={'type': 'date'}),
            'pick_up_time': forms.TimeInput(attrs={'type': 'time'}),
            'drop_off_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'instance' in kwargs:
            appointment = kwargs['instance']
            self.fields['driver'].queryset = Driver.objects.filter(
                is_available=True
            ) | Driver.objects.filter(id=appointment.driver.id if appointment.driver else None)
            

class RentalUpdateForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['car', 'customer_name', 'customer_phone', 'pick_up_time', 'drop_off_time', 'region', 'location_category', 'town', 'rental_date', 'return_date', 'document_type', 'document_number', 'driver', 'status', 'commission_rate', 'total_price']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'pick_up_time': forms.TimeInput(attrs={'type': 'time'}),
            'drop_off_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'instance' in kwargs:
            rental = kwargs['instance']
            self.fields['driver'].queryset = Driver.objects.filter(
                is_available=True
            ) | Driver.objects.filter(id=rental.driver.id if rental.driver else None)
            

class RentalPaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['car', 'customer_name', 'customer_phone', 'pick_up_time', 'drop_off_time', 'pick_up_location', 'drop_off_location', 'region', 'location_category', 'town', 'rental_date', 'return_date', 'document_type', 'document_number', 'driver', 'status', 'commission_rate', 'payment_method', 'momo_code', 'transaction_id', 'base_price', 'vat_percentage', 'vat_amount', 'total_price']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'pick_up_time': forms.TimeInput(attrs={'type': 'time'}),
            'drop_off_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'instance' in kwargs:
            rental_payment = kwargs['instance']
            self.fields['driver'].queryset = Driver.objects.filter(
                is_available=True
            ) | Driver.objects.filter(id=rental_payment.driver.id if rental_payment.driver else None)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['customer_name', 'customer_phone', 'rental_date', 'return_date', 'pick_up_location', 'drop_off_location', 'payment_method', 'transaction_id']
        
        