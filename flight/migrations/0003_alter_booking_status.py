# Generated by Django 5.1.4 on 2025-02-04 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_airline_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending', max_length=20),
        ),
    ]
