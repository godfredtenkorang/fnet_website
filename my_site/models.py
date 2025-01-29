from django.db import models
from django.utils.timezone import now
from decimal import Decimal


class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    licence_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_available = models.BooleanField(default=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # commission earned
    license_issue_date = models.DateField(null=True, blank=True)
    licence_expiry_date = models.DateField(null=True, blank=True)
    
    
    def days_of_expiry(self):
        """
        Calculate the number of days until the driver's license expires.
        Returns:
            int: Number of days until expiry. Negative if already expired.
        """
        today = now().date()
        delta = self.licence_expiry_date - today
        return delta.days
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.licence_number}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return f"{self.name}"

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
    brand = models.CharField(max_length=50)
    seats = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE)
    color = models.CharField(max_length=100)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION)
    air_conditioning = models.CharField(max_length=10, choices=AIR_CONDITIONING)
    year_manufactured = models.CharField(max_length=4)
    engine_capacity = models.CharField(max_length=100, null=True, blank=True)
    airbag = models.CharField(max_length=20, default='Available')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_within_kumasi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ahafo_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ashanti_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono_east_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    central_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eastern_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    greater_accra_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    northern_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    north_east_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    oti_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savannah_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_east_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_west_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volta_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western_north_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='Available')
    year_registered = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    
    def calculate_vat(self, price):
        return (self.vat_percentage / Decimal(100)) * price
    
    def calculate_total_with_vat(self, price):
        return price + self.calculate_vat(price)

    def __str__(self):
        return f"{self.brand} {self.car_name}"

class Gallery(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery-img/')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Galleries'
        ordering = ['-date_added']
        
    def __str__(self):
        return self.name