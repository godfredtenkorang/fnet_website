# Generated by Django 5.1.4 on 2025-01-22 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_driverssmslog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverssmslog',
            old_name='recipients',
            new_name='phone_numbers',
        ),
    ]
