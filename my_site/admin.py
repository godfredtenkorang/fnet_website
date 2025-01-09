from django.contrib import admin
from .models import Car, Category, Driver

# Register your models here.
admin.site.register(Category)
admin.site.register(Car)
admin.site.register(Driver)
