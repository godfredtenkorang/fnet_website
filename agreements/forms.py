from django import forms
from .models import *


class PayAndMoveAgreementForm(forms.ModelForm):
    class Meta:
        model = PayAndDriveAgreement
        fields = ['customer_name', 'digital_address', 'ghana_card_number', 'phone_number', 'whatsapp_number', 'vehicle_make_and_model', 'registration_number', 'color', 'mileage_at_pickup', 'start_date_and_time', 'end_date_and_time', 'pickup_location', 'return_location', 'payment_for', 'rental_charge', 'driver_accommodation_fee', 'total']
        
        
        
class DriverAgreementForm(forms.ModelForm):
    class Meta:
        model = DriverAgreement
        fields = ['driver_full_name', 'ghana_card_number', 'driving_license_number', 'license_expiration_date', 'guarantor_full_name', 'guarantor_ghana_card_number', 'date_of_birth', 'contact_number', 'residential_address', 'digital_address', 'relationship_to_driver', 'emergency_contact_number', 'representative_name']
        
        
