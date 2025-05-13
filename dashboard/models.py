from django.db import models
from users.models import User

from my_site.models import Car
from django.forms import ValidationError
from django.utils import timezone

# Create your models here.
class SMSLog(models.Model):
    recipients = models.TextField(null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, null=True, blank=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    
    
# Create your models here.
class DriversSMSLog(models.Model):
    recipients = models.TextField(null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, null=True, blank=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    
class Customer(models.Model):
    name = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=20)
    
    
    def __str__(self):
        return f"{self.name} - {self.phone_number}"
    

class LoadCarImagesForCustomer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer}"
    





class MileageRecord(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_mileage = models.PositiveIntegerField()
    end_mileage = models.PositiveIntegerField(null=True, blank=True)
    
    def clean(self):
        if self.end_mileage is not None and self.start_mileage is not None:
            if self.end_mileage < self.start_mileage:
                raise ValidationError("End mileage must be greater than start mileage")

    
    @property
    def mileage_used(self):
        if self.end_mileage is None:
            return None
        return self.end_mileage - self.start_mileage
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update vehicle's oil change status
        self.vehicle.refresh_from_db()
        if self.vehicle.needs_oil_change:
            self.create_oil_change_notification()
        
    def create_oil_change_notification(self):
        Notification.objects.create(
            driver=self.driver,
            message=f"Oil change needed for {self.vehicle} (Current: {self.end_mileage}km)",
            notification_type="maintenance"
        )
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date}: {self.vehicle} - {self.mileage_used} km"
    
class FuelRecord(models.Model):
    STATION_NAME = [
        ('Shell', 'Shell'),
        ('Goil', 'Goil'),
        ('Total', 'Total'),
        ('ZEN', 'ZEN'),
    ]
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    liters = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    station_name = models.CharField(max_length=100, choices=STATION_NAME, null=True, blank=True)
    receipt = models.FileField(upload_to='fuel_receipts/', blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date}: {self.liters}L - {self.amount}"


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('toll', 'Toll Fee'),
        ('parking', 'Parking Fee'),
        ('other', 'Other'),
    ]
    
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.FileField(upload_to='expense_receipts/', blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date}: {self.get_type_display()} - {self.amount}"
    
    
class OilChange(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    mileage = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        
        if is_new:
            # Update the vehicle's last oil change info when saving
            self.vehicle.last_oil_change_mileage = self.mileage
            self.vehicle.last_oil_change_date = self.date
            self.vehicle.save()
            
            # Clear any oil change notifications for this vehicle
            Notification.objects.filter(
                driver=self.driver,
                notification_type="maintenance",
                message__contains=str(self.vehicle)
            ).update(is_read=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date}: {self.vehicle} - {self.mileage} km"
    
class Notification(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.driver}: {self.message[:50]}..."