# Generated by Django 5.1.4 on 2025-01-17 15:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0009_expense'),
        ('my_site', '0008_car_year_registered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='drivers_commission',
        ),
        migrations.AlterField(
            model_name='expense',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='my_site.car'),
        ),
    ]
