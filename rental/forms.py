from django import forms
from .models import Appointment, Payment, Rental
from my_site.models import Driver


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['car', 'customer_name', 'customer_phone', 'schedule_date', 'pick_up_time', 'drop_off_time', 'pick_up_location', 'drop_off_location', 'gps_address', 'driver', 'agent', 'status', 'commission_rate', 'purpose', 'total_price']
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
            
    def __init__(self, *args, **kwargs):
        super(AppointmentUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['car'].widget.attrs['disabled'] = 'disabled'
        self.fields['customer_name'].widget.attrs['readonly'] = 'readonly'
        self.fields['customer_phone'].widget.attrs['readonly'] = 'readonly'
        self.fields['schedule_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['pick_up_time'].widget.attrs['readonly'] = 'readonly'
        self.fields['drop_off_time'].widget.attrs['readonly'] = 'readonly'
        self.fields['pick_up_location'].widget.attrs['readonly'] = 'readonly'
        self.fields['drop_off_location'].widget.attrs['readonly'] = 'readonly'
        self.fields['gps_address'].widget.attrs['readonly'] = 'readonly'
        self.fields['purpose'].widget.attrs['readonly'] = 'readonly'
        # self.fields['total_price'].widget.attrs['readonly'] = 'readonly'
            

class RentalUpdateForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['customer', 'car', 'customer_name', 'customer_phone', 'pick_up_time', 'drop_off_time', 'location_category', 'town', 'number_of_days', 'rental_date', 'return_date', 'document_type', 'document_number', 'driver', 'agent', 'status', 'commission_rate', 'agent_commission_rate', 'vat_percentage', 'base_price', 'vat_amount', 'transaction_id', 'total_price']
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
            
    def __init__(self, *args, **kwargs):
        super(RentalUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['car'].widget.attrs['disabled'] = 'disabled'
        self.fields['customer_name'].widget.attrs['readonly'] = 'readonly'
        self.fields['customer_phone'].widget.attrs['readonly'] = 'readonly'
        self.fields['pick_up_time'].widget.attrs['readonly'] = 'readonly'
        self.fields['drop_off_time'].widget.attrs['readonly'] = 'readonly'
        self.fields['location_category'].widget.attrs['readonly'] = 'readonly'
        self.fields['town'].widget.attrs['readonly'] = 'readonly'
        self.fields['rental_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['return_date'].widget.attrs['readonly'] = 'readonly'
        # self.fields['document_type'].widget.attrs['disabled'] = 'disabled'
        self.fields['document_number'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        # self.fields['total_price'].widget.attrs['readonly'] = 'readonly'
 

class RentalPaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['car', 'customer_name', 'customer_phone', 'pick_up_time', 'drop_off_time', 'pick_up_location', 'drop_off_location', 'location_category', 'town', 'rental_date', 'return_date', 'document_type', 'document_number', 'driver', 'agent', 'status', 'commission_rate', 'payment_method', 'momo_code', 'transaction_id', 'base_price', 'vat_percentage', 'vat_amount', 'total_price']
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
            
    def __init__(self, *args, **kwargs):
        super(RentalPaymentUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['car'].widget.attrs['disabled'] = 'disabled'
        self.fields['customer_name'].widget.attrs['readonly'] = 'readonly'
        self.fields['customer_phone'].widget.attrs['readonly'] = 'readonly'
        self.fields['pick_up_time'].widget.attrs['readonly'] = 'readonly'
        self.fields['drop_off_time'].widget.attrs['readonly'] = 'readonly'
        self.fields['pick_up_location'].widget.attrs['readonly'] = 'readonly'
        self.fields['drop_off_location'].widget.attrs['readonly'] = 'readonly'
        self.fields['location_category'].widget.attrs['readonly'] = 'readonly'
        self.fields['town'].widget.attrs['readonly'] = 'readonly'
        self.fields['rental_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['return_date'].widget.attrs['readonly'] = 'readonly'
        # self.fields['document_type'].widget.attrs['disabled'] = 'disabled'
        self.fields['document_number'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['payment_method'].widget.attrs['readonly'] = 'readonly'
        # self.fields['momo_code'].widget.attrs['disabled'] = 'disabled'
        self.fields['transaction_id'].widget.attrs['readonly'] = 'readonly'
        self.fields['base_price'].widget.attrs['readonly'] = 'readonly'
        self.fields['vat_percentage'].widget.attrs['readonly'] = 'readonly'
        self.fields['vat_amount'].widget.attrs['readonly'] = 'readonly'
        # self.fields['total_price'].widget.attrs['readonly'] = 'readonly'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['customer_name', 'customer_phone', 'rental_date', 'return_date', 'pick_up_location', 'drop_off_location', 'payment_method', 'transaction_id']
        
        