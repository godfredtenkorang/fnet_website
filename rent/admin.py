from django.contrib import admin
from .models import Property, PropertyBooking

# Register your models here.
admin.site.register(Property)
admin.site.register(PropertyBooking)