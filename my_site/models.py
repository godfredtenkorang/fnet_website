from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now
from decimal import Decimal
from users.models import User

from django.utils import timezone


class Agent(models.Model):
    agent = models.OneToOneField(User, models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ghana_card = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"

class Driver(models.Model):
    driver = models.OneToOneField(User, models.CASCADE, null=True, blank=True, related_name='driver')
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
        return f"{self.driver} - {self.phone_number}"
    
class DriverReview(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1,6)]) # 1 to 5 stars
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.driver.first_name} by {self.customer.username}"

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
        ('Unlimited', 'Unlimited'),
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
    price_per_km = models.DecimalField(max_digits=10 ,decimal_places=2, default=0.00)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_within_kumasi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_within_kumasi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ahafo_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_ahafo_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ashanti_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_ashanti_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_bono_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono_east_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_bono_east_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    central_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_central_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eastern_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_eastern_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    greater_accra_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_greater_accra_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    northern_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_northern_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    north_east_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_north_east_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    oti_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_oti_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savannah_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_savannah_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_east_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_upper_east_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_west_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_upper_west_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volta_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_volta_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_western_region= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western_north_region_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    range_price_western_north_region = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='Available')
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    year_registered = models.CharField(max_length=10, null=True, blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    oil_change_default = models.PositiveBigIntegerField(default=5000, help_text="Default mileage between oil changes (km)")
    last_oil_change_mileage = models.PositiveBigIntegerField(default=0, help_text="Mileage at last oil change (km)")
    last_oil_change_date = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    
    
    def clean(self):
        if self.last_oil_change_mileage is not None and self.current_mileage is not None:
            if self.last_oil_change_mileage > self.current_mileage:
                raise ValidationError("Last oil change mileage cannot be greater than current mileage")
            
    def reset_oil_change_tracking(self, current_tracking):
        self.last_oil_change_mileage = current_tracking
        self.last_oil_change_date = timezone.now().date()
        self.save()
        
        
    
    @property
    def mileage_until_oil_change(self):
        # Ensure we have valid values for calculation
        if self.last_oil_change_mileage is None:
            return self.oil_change_default  # If never changed, use full interval
            
        current_mileage = self.current_mileage
        if current_mileage is None:
            return 0  # Can't calculate without current mileage
            
        miles_since_change = current_mileage - self.last_oil_change_mileage
        remaining = self.oil_change_default - miles_since_change
        return max(remaining, 0)  # Don't return negative numbers
    
    @property
    def current_mileage(self):
        """Get the current mileage from the latest record"""
        if not self.pk:  # If instance isn't saved yet
            return None
        latest_record = self.mileagerecord_set.order_by('-date').first()
        return latest_record.end_mileage if latest_record else None
    
    @property
    def miles_since_last_oil_change(self):
        """How many miles driven since last oil change"""
        if self.last_oil_change_mileage is None or self.current_mileage is None:
            return 0
        return self.current_mileage - self.last_oil_change_mileage
    
    @property
    def needs_oil_change(self):
        if self.mileage_until_oil_change == 0:
            return True
        return False
    
    # def calculate_vat(self, price):
    #     return (self.vat_percentage / Decimal(100)) * price
    
    # def calculate_total_with_vat(self, price):
    #     return price + self.calculate_vat(price)

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