# Generated by Django 5.1.4 on 2025-02-16 04:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0053_rental_agent_commission_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Bank', 'Bank'), ('MoMo', 'MoMo')], max_length=100)),
                ('payment_code', models.CharField(choices=[('1441002567287', '1441002567287'), ('0550222888', '0550222888')], max_length=100)),
                ('transaction_id', models.CharField(max_length=20)),
                ('is_approved', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.rental')),
            ],
        ),
    ]
