# Generated by Django 5.1.4 on 2025-01-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0009_appointment_car_appointment_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='customer_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
