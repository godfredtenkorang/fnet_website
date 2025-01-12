from django.contrib import admin
from .models import Rental, Appointment, Contact, Payment

# Register your models here.
admin.site.register(Rental)
admin.site.register(Appointment)
admin.site.register(Contact)
admin.site.register(Payment)