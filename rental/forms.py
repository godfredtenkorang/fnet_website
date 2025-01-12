from django import forms
from .models import Appointment, Payment
from my_site.models import Driver


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['car','appointment_date', 'appointment_time', 'pick_up_location', 'drop_off_location', 'gps_address', 'driver', 'status', 'commission_rate', 'purpose']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'instance' in kwargs:
            appointment = kwargs['instance']
            self.fields['driver'].queryset = Driver.objects.filter(
                is_available=True
            ) | Driver.objects.filter(id=appointment.driver.id if appointment.driver else None)
        

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['customer_name', 'customer_email', 'customer_phone', 'rental_date', 'return_date', 'pick_up_location', 'drop_off_location', 'payment_method', 'transaction_id']
        
        