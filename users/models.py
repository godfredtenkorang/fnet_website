from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(unique=True, max_length=15)
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("driver", "Driver"),
        ("agent", "Agent"),
        ("admin", "Admin")
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")
    
    REQUIRED_FIELDS = ['phone']
    USERNAME_FIELD = 'username'
    
    
    def __str__(self):
        return self.username