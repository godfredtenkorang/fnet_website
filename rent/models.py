from django.db import models
from django.utils import timezone
from users.models import User
# Create your models here.

AVAILABILITY_STATUS = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]



class Property(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    number_of_rooms = models.CharField(max_length=20, default='', blank=True)
    number_of_bathrooms = models.CharField(max_length=20, default='', blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='properties/')
    image2 = models.ImageField(upload_to='properties/')
    image3 = models.ImageField(upload_to='properties/')
    image4 = models.ImageField(upload_to='properties/')
    image5 = models.ImageField(upload_to='properties/', default="")
    available = models.CharField(max_length=100, choices=AVAILABILITY_STATUS, default='Available')
    amenity1 = models.CharField(max_length=100, default='', blank=True)
    amenity2 = models.CharField(max_length=100, default='', blank=True)
    amenity3 = models.CharField(max_length=100, default='', blank=True)
    amenity4 = models.CharField(max_length=100, default='', blank=True)
    amenity5 = models.CharField(max_length=100, default='', blank=True)
    amenity6 = models.CharField(max_length=100, default='', blank=True)
    amenity7 = models.CharField(max_length=100, default='', blank=True)
    amenity8 = models.CharField(max_length=100, default='', blank=True)
    amenity9 = models.CharField(max_length=100, default='', blank=True)
    amenity10 = models.CharField(max_length=100, default='', blank=True)
    slug = models.SlugField(unique=True, blank=True, default='')
    


    def __str__(self):
        return self.title

class PropertyBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    check_in_date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_date = models.DateField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.property.title}"