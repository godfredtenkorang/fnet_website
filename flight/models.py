from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='airlines/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    category = models.CharField(max_length=100, choices=[('One Way', 'One Way'), ('Roundtrip', 'Roundtrip')], default='One Way')
    trip_from = models.CharField(max_length=100, choices=[('Accra', 'Accra'), ('Kumasi', 'Kumasi')])
    trip_to = models.CharField(max_length=100, choices=[('Accra', 'Accra'), ('Kumasi', 'Kumasi')])
    trip_departure = models.DateField()
    trip_return = models.DateField(null=True, blank=True)
    number_of_adults = models.PositiveIntegerField(default=0)
    number_of_children = models.PositiveIntegerField(default=0)
    number_of_infants = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending')

    def __str__(self):
        return f"Booking by {self.full_name} - {self.phone_number}"
