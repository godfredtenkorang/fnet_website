# Generated by Django 5.1.4 on 2025-01-18 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0024_alter_region_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='location_category',
            field=models.CharField(default='', max_length=100),
        ),
    ]
