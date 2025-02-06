# Generated by Django 5.1.4 on 2025-02-05 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('price_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image1', models.ImageField(upload_to='properties/')),
                ('image2', models.ImageField(upload_to='properties/')),
                ('image3', models.ImageField(upload_to='properties/')),
                ('image4', models.ImageField(upload_to='properties/')),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_approved', models.BooleanField(default=False)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent.property')),
            ],
        ),
    ]
