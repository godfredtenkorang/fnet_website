# Generated by Django 5.1.4 on 2025-02-02 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0041_alter_rental_base_price_alter_rental_vat_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='vat_percentage',
            field=models.DecimalField(decimal_places=2, default=2.5, max_digits=5),
        ),
    ]
