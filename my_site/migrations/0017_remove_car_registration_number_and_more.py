# Generated by Django 5.1.4 on 2025-01-29 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0016_remove_car_bluetooth_connectivity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='registration_number',
        ),
        migrations.RemoveField(
            model_name='car',
            name='vat_percentage',
        ),
    ]
