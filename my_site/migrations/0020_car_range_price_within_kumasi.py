# Generated by Django 5.1.4 on 2025-01-30 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0019_alter_gallery_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='range_price_within_kumasi',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
