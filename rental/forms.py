from django import forms
from .models import Appointment
from my_site.models import Driver


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['car','appointment_date', 'appointment_time', 'pick_up_location', 'drop_off_location', 'gps_address', 'driver', 'status', 'purpose']
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
        
        