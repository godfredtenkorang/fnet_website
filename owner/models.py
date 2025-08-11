from django.db import models
from users.models import User


class Owner(models.Model):
    owner = models.OneToOneField(User, models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ghana_card = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"