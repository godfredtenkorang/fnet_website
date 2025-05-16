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
    

