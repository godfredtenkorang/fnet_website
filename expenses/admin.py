from django.contrib import admin
from .models import MyCar, Expense, Receipt

# Register your models here.
admin.site.register(MyCar)
admin.site.register(Expense)
admin.site.register(Receipt)