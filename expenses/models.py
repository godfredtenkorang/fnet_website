from django.db import models
from rental.models import Car

class MyCar(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
MONTHS = [
    ('January', 'January'),
    ('Febuary', 'Febuary'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
]

class Expense(models.Model):
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='expenses')
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    other_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20, choices=MONTHS)

    def __str__(self):
        return f"{self.car.car_name} - {self.date}"
    

class Receipt(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Service(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    mileage = models.CharField(max_length=100)
    fuel = models.CharField(max_length=100)
    expense= models.CharField(max_length=225)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Services for {self.car} - Mileage {self.mileage}"