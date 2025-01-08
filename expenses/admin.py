from django.contrib import admin
from .models import MyCar, Expense

# Register your models here.
admin.site.register(MyCar)
admin.site.register(Expense)