from django.db import models

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