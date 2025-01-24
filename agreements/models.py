from django.db import models

# Create your models here.
class Contact(models.Model):
    # Customer information
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    digital_address = models.CharField(max_length=100)
    ghana_card_number = models.CharField(max_length=15)
    # Guarantor Information (for Self-Drive)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    digital_address = models.CharField(max_length=100, null=True, blank=True)
    relationship_to_customer = models.CharField(max_length=100)
    ghana_card_number = models.CharField(max_length=15)
    