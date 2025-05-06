from django.contrib import admin
from .models import SMSLog, DriversSMSLog, LoadCarImagesForCustomer, MileageRecord, Expense, OilChange, FuelRecord

# Register your models here.
admin.site.register(SMSLog)
admin.site.register(DriversSMSLog)


admin.site.register(LoadCarImagesForCustomer)

admin.site.register(MileageRecord)
admin.site.register(FuelRecord)
admin.site.register(Expense)
admin.site.register(OilChange)