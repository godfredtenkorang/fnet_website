from django.contrib import admin
from .models import Airline, Booking

# Register your models here.
admin.site.register(Airline)
admin.site.register(Booking)