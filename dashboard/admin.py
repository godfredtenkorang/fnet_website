from django.contrib import admin
from .models import SMSLog, DriversSMSLog, LoadCarImagesForCustomer

# Register your models here.
admin.site.register(SMSLog)
admin.site.register(DriversSMSLog)


admin.site.register(LoadCarImagesForCustomer)

