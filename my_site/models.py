from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Car(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Truck', 'Truck'),
        ('Convertible', 'Convertible'),
    ]

    AVAILABILITY_STATUS = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]
    
    FUEL_TYPE = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
    ]
    
    TRANSMISSION = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manuel'),
    ]
    
    AIR_CONDITIONING = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    BLUETOOTH_CONNECTTIVITY = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars', null=True)
    car_name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    registration_number = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=50)
    seats = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE)
    color = models.CharField(max_length=100)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION)
    mileage = models.CharField(max_length=20)
    air_conditioning = models.CharField(max_length=10, choices=AIR_CONDITIONING)
    year_manufactured = models.CharField(max_length=4)
    gps_navigation = models.CharField(max_length=20, default='Included')
    airbag = models.CharField(max_length=20, default='Available')
    bluetooth_connectivity = models.CharField(max_length=10, choices=BLUETOOTH_CONNECTTIVITY)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='Available')
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.brand} {self.car_name} ({self.registration_number})"

