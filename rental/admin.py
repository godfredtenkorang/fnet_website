from django.contrib import admin
from .models import Rental, Appointment, Contact, Payment, Region

# Register your models here.
admin.site.register(Rental)
admin.site.register(Appointment)
admin.site.register(Contact)
admin.site.register(Payment)
admin.site.register(Region)