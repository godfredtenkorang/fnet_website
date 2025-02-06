from django import forms
from .models import Booking


class UpdateFlightBooking(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['airline', 'full_name', 'phone_number', 'category', 'trip_from', 'trip_to', 'trip_departure', 'trip_return', 'number_of_adults', 'number_of_children', 'number_of_infants', 'status']
        widgets = {
            'trip_departure': forms.DateInput(attrs={'type': 'date'}),
            'trip_return': forms.DateInput(attrs={'type': 'date'}),
        }