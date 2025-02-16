from django.db import models
from my_site.models import Car, Driver, Agent
import uuid
from decimal import Decimal
from dashboard.models import Customer
from users.models import User

    
class Region(models.Model):
    REGIONS = [
        ('⁠Ashanti Region', '⁠Ashanti Region'),
        ('⁠Greater Accra Region', ' ⁠Greater Accra Region'),
        ('Western Region', 'Western Region'),
        ('Western North Region', 'Western North Region'),
        ('Central Region', 'Central Region'),
        ('Eastern Region', 'Eastern Region'),
        ('⁠Volta Region', '⁠Volta Region'),
        ('Oti Region', 'Oti Region'),
        ('⁠Northern Region', '⁠Northern Region'),
        ('⁠Savannah Region', '⁠Savannah Region'),
        ('North East Region', 'North East Region'),
        ('Upper East Region', 'Upper East Region'),
        ('⁠Upper West Region', '⁠Upper West Region'),
        ('Bono Region', 'Bono Region'),
        ('Bono East Region', 'Bono East Region'),
        ('Ahafo Region', 'Ahafo Region'),
    ]
    name = models.CharField(max_length=100, choices=REGIONS)

    def __str__(self):
        return self.name


class Rental(models.Model):
    DOCUMENT_TYPE = [
        ('Ghana Card', 'Ghana Card'),
        ('Passport', 'Passport'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    emergency_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_phone = models.CharField(max_length=15, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    location_category = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    town = models.CharField(max_length=250, default='')
    pick_up_time = models.TimeField(null=True, blank=True)
    drop_off_time = models.TimeField(null=True, blank=True)
    number_of_days = models.CharField(max_length=250, null=True, blank=True)
    rental_date = models.DateField()
    return_date = models.DateField()
    total_price = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE, default='Ghana Card')
    document_number = models.CharField(max_length=100, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='rentals')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='rentals')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12.50)
    agent_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)
    base_price = models.CharField(max_length=100, blank=True, null=True)
    vat_amount = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        
    def calculate_commission(self):
        if self.driver:
            rental_fee = Decimal(self.total_price)  # Assuming car has a `daily_rate` field
            return (rental_fee * self.commission_rate) / 100
        return 0.00
    
    def calculate_agent_commission(self):
        if self.agent:
            rental_fee = Decimal(self.total_price)  # Assuming car has a `daily_rate` field
            return (rental_fee * self.agent_commission_rate) / 100
        return 0.00
        
    def is_negotiable(self):
        """Returns True if the rental period is more than 3 days, otherwise False."""
        if self.return_date and self.rental_date:
            duration = (self.return_date - self.rental_date).days
            return duration > 3
        return False
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate a unique invoice number, e.g., INV20250104-XXXX
            super().save(*args, **kwargs)
            self.invoice_number = f"TL/IN/{self.updated_at.strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rental by {self.customer_name} for {self.car}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, related_name='appointments')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    schedule_date = models.DateField()
    pick_up_time = models.TimeField(null=True, blank=True)
    drop_off_time = models.TimeField(null=True, blank=True)
    pick_up_location = models.CharField(max_length=250, null=True)
    drop_off_location = models.CharField(max_length=250, null=True)
    gps_address = models.CharField(max_length=100, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    purpose = models.TextField(null=True, blank=True)  # e.g., "Test drive", "Car inspection", etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12.50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        ordering = ['-created_at']
        
            

    def __str__(self):
        return f"Schedule ride with {self.customer_name} on {self.schedule_date} at {self.pick_up_time} - GH¢ {self.total_price:.2f}"
    

    
class Payment(models.Model):
    DOCUMENT_TYPE = [
        ('Ghana Card', 'Ghana Card'),
        ('Passport', 'Passport'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='payments')
    rental_date = models.DateField()
    return_date = models.DateField()
    location_category = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    town = models.CharField(max_length=250, default='')
    pick_up_time = models.TimeField(null=True, blank=True)
    drop_off_time = models.TimeField(null=True, blank=True)
    pick_up_location = models.CharField(max_length=100, null=True, blank=True)
    drop_off_location = models.CharField(max_length=100, null=True, blank=True)
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE, default='Ghana Card')
    document_number = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    momo_code = models.CharField(max_length=50, null=True, blank=True, choices=[('123456', '123456')])
    transaction_id = models.CharField(max_length=50)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=25.00)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_successful = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate a unique invoice number, e.g., INV20250104-XXXX
            super().save(*args, **kwargs)
            self.invoice_number = f"TL/IN/{self.updated_at.strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)
        
    

    def __str__(self):
        return f"Payment by {self.customer_name} for {self.car} - {self.total_price}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    
    class Meta:
        ordering = ['-name']
    
    def __str__(self):
        return f"New contact from {self.name} - {self.phone}"
    

class RentalPayment(models.Model):
    PAYMENT_METHOD = [
        ('Bank', 'Bank'),
        ('MoMo', 'MoMo'),
    ]
    PAYMENT_CODE = [
        ('1441002567287', '1441002567287'),
        ('0597406474', '0597406474'),
    ]
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD)
    payment_code = models.CharField(max_length=100, choices=PAYMENT_CODE)
    transaction_id = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.rental.customer_name} - {self.transaction_id} for {self.rental.car}"