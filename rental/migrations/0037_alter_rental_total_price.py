# Generated by Django 5.1.4 on 2025-01-30 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0036_remove_payment_region_remove_rental_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='total_price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
