# Generated by Django 5.1.4 on 2025-01-22 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_recipients_driverssmslog_phone_numbers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverssmslog',
            old_name='phone_numbers',
            new_name='recipients',
        ),
    ]
