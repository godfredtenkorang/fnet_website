from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image

class User(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(unique=True, max_length=10)
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

    
    
class OTP(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    
    
    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300 # Valid for 5 minutes
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)