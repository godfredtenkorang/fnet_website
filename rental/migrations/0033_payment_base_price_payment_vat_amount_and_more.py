# Generated by Django 5.1.4 on 2025-01-20 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0032_payment_driver_rental_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='base_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='vat_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='vat_percentage',
            field=models.DecimalField(decimal_places=2, default=25.0, max_digits=5),
        ),
    ]
