# Generated by Django 5.1.4 on 2025-06-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0030_alter_car_availability_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='registration_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
