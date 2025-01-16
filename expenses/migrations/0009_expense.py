# Generated by Django 5.1.4 on 2025-01-16 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0008_delete_expense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount_received', models.DecimalField(decimal_places=2, max_digits=10)),
                ('drivers_commission', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_expenses', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('month', models.CharField(max_length=20)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='expenses.mycar')),
            ],
        ),
    ]
