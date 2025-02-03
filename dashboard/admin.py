from django.contrib import admin
from .models import SMSLog, Customer, DriversSMSLog, LoadCarImagesForCustomer

# Register your models here.
admin.site.register(SMSLog)
admin.site.register(DriversSMSLog)


class LoadCarImagesForCustomerInLine(admin.TabularInline):
    model = LoadCarImagesForCustomer
    extra = 3
    
  
  
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'phone_number']})]
    inlines = [LoadCarImagesForCustomerInLine]
  
  
admin.site.register(Customer, CustomerAdmin)