# Generated by Django 5.1.4 on 2025-01-10 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0016_payment_momo_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='momo_code',
            field=models.CharField(blank=True, choices=[('123456', '123456')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=50),
        ),
    ]
