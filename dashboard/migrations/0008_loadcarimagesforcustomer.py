# Generated by Django 5.1.4 on 2025-02-02 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_rename_phone_numbers_driverssmslog_recipients'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadCarImagesForCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='car_images/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
    ]
