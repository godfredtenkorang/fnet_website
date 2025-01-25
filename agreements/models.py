from django.db import models

# Create your models here.
class ContactForm(models.Model):
    # Customer information
    customer_title = models.CharField(max_length=100, default="Customer Information")
    customer_full_name = models.CharField(max_length=100)
    customer_phone_number = models.CharField(max_length=15)
    customer_whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    customer_digital_address = models.CharField(max_length=100)
    customer_ghana_card_number = models.CharField(max_length=15)
    # Guarantor Information (for Self-Drive)
    guarantor_title = models.CharField(max_length=100, default="Guarantor Information (for Self-Drive)")
    guarantor_full_name = models.CharField(max_length=100)
    guarantor_phone_number = models.CharField(max_length=15)
    guarantor_digital_address = models.CharField(max_length=100, null=True, blank=True)
    guarantor_relationship_to_customer = models.CharField(max_length=100)
    guarantor_ghana_card_number = models.CharField(max_length=15)
    # Emergency Contact Information (for Pay and Drive)
    emergency_title = models.CharField(max_length=100, default="Emergency Contact Information (for Pay and Drive)")
    emergency_full_name = models.CharField(max_length=100)
    emergency_phone_number = models.CharField(max_length=15)
    emergency_relationship_to_customer = models.CharField(max_length=50)
    # Vehicle Details
    vehicle_title = models.CharField(max_length=100, default='Vehicle Details')
    vehicle_type = models.CharField(max_length=100)
    vehicle_registration = models.CharField(max_length=100)
    # Vehicle Rental Details
    rental_title = models.CharField(max_length=100, default='Vehicle Rental Details')
    service_type = models.CharField(max_length=100, choices=[("Drive and Pay(Self-Drive)", "Drive and Pay(Self-Drive)"), ("Pay and Drive(Company Driver)", "Pay and Drive(Company Driver)")])
    return_duration = models.CharField(max_length=10)
    start_date_and_time = models.DateTimeField(auto_now_add=True)
    end_date_and_time = models.DateTimeField(auto_now_add=True)
    # Payment Information
    payment_title = models.CharField(max_length=100, default='Payment Information')
    self_drive_daily_charge = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.CharField(max_length=10)
    hours = models.CharField(max_length=20)
    cash_lock = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_payment_due = models.DecimalField(max_digits=10, decimal_places=2)
    pay_and_drive_daily_charge = models.DecimalField(max_digits=10, decimal_places=2)
    pay_and_drive_mileage = models.CharField(max_length=10)
    pay_and_drive_hours = models.CharField(max_length=20)
    pay_and_drive_total_payment_due = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices=[("Cash", "Cash"), ("Mobile Money (MoMo)", "Mobile Money (MoMo)"), ("Bank Transfer", "Bank Transfer")])
    # Payment Terms
    terms_title = models.CharField(max_length=100, default='Payment Terms')
    terms_self_drive_daily_charge = models.DecimalField(max_digits=10, decimal_places=2)
    terms_mileage = models.CharField(max_length=10)
    refundable_cash = models.DecimalField(max_digits=10, decimal_places=2)
    terms_pay_and_drive_daily_charge = models.DecimalField(max_digits=10, decimal_places=2)
    terms_pay_and_drive_mileage = models.CharField(max_length=10)
    # Mileage Policy
    mileage_policy = models.CharField(max_length=20)
    # Cash Lock Return (Self-Drive Only)
    cash_lock_policy = models.DecimalField(max_digits=10, decimal_places=2)
    
    
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