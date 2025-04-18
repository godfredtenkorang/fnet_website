# Generated by Django 5.1.4 on 2025-01-17 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0019_alter_contact_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='appointment_date',
            new_name='schedule_date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='drop_off_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='pick_up_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
