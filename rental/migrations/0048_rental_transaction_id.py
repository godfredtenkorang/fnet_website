# Generated by Django 5.1.4 on 2025-02-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0047_remove_rental_is_returned_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
