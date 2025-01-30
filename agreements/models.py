from django.db import models
from django.utils import timezone

# Create your models here.
class BoggasForm(models.Model):
    # Customer information
    customer_title = models.CharField(max_length=100, default="Customer Information")
    customer_full_name = models.CharField(max_length=100)
    customer_phone_number = models.CharField(max_length=15)
    customer_whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    customer_digital_address = models.CharField(max_length=100)
    customer_ghana_card_number = models.CharField(max_length=15)
    customer_passport_number = models.CharField(max_length=100, null=True, blank=True)
    # Guarantor Information (for Self-Drive)
    guarantor_title = models.CharField(max_length=100, default="Guarantor Information (for Self-Drive)")
    guarantor_full_name = models.CharField(max_length=100)
    guarantor_phone_number = models.CharField(max_length=15)
    guarantor_digital_address = models.CharField(max_length=100, null=True, blank=True)
    guarantor_relationship_to_customer = models.CharField(max_length=100)
    guarantor_ghana_card_number = models.CharField(max_length=15)
    # Vehicle Details
    vehicle_title = models.CharField(max_length=100, default='Vehicle Details')
    vehicle_type = models.CharField(max_length=100)
    vehicle_registration = models.CharField(max_length=100)
    # Vehicle Rental Details
    rental_title = models.CharField(max_length=100, default='Vehicle Rental Details')
    return_duration = models.CharField(max_length=10)
    start_date_and_time = models.DateTimeField(timezone.now)
    end_date_and_time = models.DateTimeField(timezone.now)
    # Payment Information
    payment_title = models.CharField(max_length=100, default='Payment Information')
    self_drive_daily_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_payment_due = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100, choices=[("Cash", "Cash"), ("Mobile Money (MoMo)", "Mobile Money (MoMo)"), ("Bank Transfer", "Bank Transfer")])
    
    staff_name = models.CharField(max_length=100, default='')
    
    
    def __str__(self):
        return self.customer_full_name
    

class DriverAgreement(models.Model):
    # Driver Identification
    driver_full_name = models.CharField(max_length=100)
    ghana_card_number = models.CharField(max_length=20)
    driving_license_number = models.CharField(max_length=20)
    license_expiration_date = models.DateField()
    # Guarantor Information
    guarantor_full_name = models.CharField(max_length=100)
    guarantor_ghana_card_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    residential_address = models.CharField(max_length=100)
    digital_address = models.CharField(max_length=100)
    relationship_to_driver = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    representative_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.driver_full_name
    
class PayAndDriveAgreement(models.Model):
    customer_name = models.CharField(max_length=100)
    digital_address = models.CharField(max_length=20)
    ghana_card_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    # Vehicle Details
    vehicle_make_and_model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    mileage_at_pickup = models.CharField(max_length=100)
    # Rental Period
    start_date_and_time = models.DateField()
    end_date_and_time = models.DateField()
    pickup_location = models.CharField(max_length=100)
    return_location = models.CharField(max_length=100)
    # Total Payment Breakdown
    payment_for = models.CharField(max_length=100)
    rental_charge = models.DecimalField(max_digits=10, decimal_places=2)
    driver_accommodation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.customer_name