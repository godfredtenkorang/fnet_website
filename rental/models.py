from django.db import models
from my_site.models import Car, Driver
import uuid
from decimal import Decimal
from dashboard.models import Customer

    
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='rentals', null=True, blank=True)
    location_category = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    town = models.CharField(max_length=250, default='')
    pick_up_time = models.TimeField(null=True, blank=True)
    drop_off_time = models.TimeField(null=True, blank=True)
    rental_date = models.DateField()
    return_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE, default='Ghana Card')
    document_number = models.CharField(max_length=100, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='rentals')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rental by {self.customer_name} for {self.car}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    purpose = models.TextField(null=True, blank=True)  # e.g., "Test drive", "Car inspection", etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='payments')
    rental_date = models.DateField()
    return_date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    location_category = models.CharField(max_length=100, default='')
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=25.00)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
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