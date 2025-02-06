from django.db import models

# Create your models here.

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='properties/')
    image2 = models.ImageField(upload_to='properties/')
    image3 = models.ImageField(upload_to='properties/')
    image4 = models.ImageField(upload_to='properties/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"