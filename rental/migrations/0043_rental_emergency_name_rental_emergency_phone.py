# Generated by Django 5.1.4 on 2025-02-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0042_rental_emergency_name_rental_emergency_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='emergency_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='emergency_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
