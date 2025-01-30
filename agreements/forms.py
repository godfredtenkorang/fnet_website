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
        
        
class BoggasAgreementForm(forms.ModelForm):
    class Meta:
        model = BoggasForm
        fields = ['customer_full_name', 'customer_phone_number', 'customer_whatsapp_number', 'customer_digital_address', 'customer_ghana_card_number', 'guarantor_ghana_card_number', 'customer_passport_number', 'guarantor_full_name', 'guarantor_phone_number', 'guarantor_digital_address', 'guarantor_relationship_to_customer', 'guarantor_ghana_card_number', 'vehicle_type', 'vehicle_registration', 'return_duration', 'start_date_and_time', 'end_date_and_time', 'self_drive_daily_charge', 'total_payment_due', 'payment_method', 'staff_name']
        
        