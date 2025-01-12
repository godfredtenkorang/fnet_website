from django.db import models

class MyCar(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    date = models.DateField()
    car = models.ForeignKey(MyCar, on_delete=models.CASCADE, related_name='expenses')
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    drivers_commission = models.DecimalField(max_digits=10, decimal_places=2)
    other_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.car.name} - {self.date}"
    

class Receipt(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name