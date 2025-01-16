from django.db import models
from my_site.models import Car, Driver
import uuid


class Rental(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=15)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    rental_date = models.DateField()
    return_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
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
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, related_name='appointments')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=15)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    pick_up_location = models.CharField(max_length=250, null=True)
    drop_off_location = models.CharField(max_length=250, null=True)
    gps_address = models.CharField(max_length=100, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    purpose = models.TextField(null=True, blank=True)  # e.g., "Test drive", "Car inspection", etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    
    
    class Meta:
        ordering = ['-created_at']
        
    def calculate_commission(self):
        if self.car and self.driver:
            rental_fee = self.car.price_per_day
            return (rental_fee * self.commission_rate) / 100
        return 0.00
            

    def __str__(self):
        return f"Appointment with {self.customer_name} on {self.appointment_date} at {self.appointment_time}"
    

    
class Payment(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=15)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='payments')
    rental_date = models.DateField()
    return_date = models.DateField()
    pick_up_location = models.CharField(max_length=100, null=True, blank=True)
    drop_off_location = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    momo_code = models.CharField(max_length=50, null=True, blank=True, choices=[('123456', '123456')])
    transaction_id = models.CharField(max_length=50)
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