# Generated by Django 5.1.4 on 2025-01-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0022_region_rental_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(choices=[('\u2060Greater Accra Region', ' \u2060Greater Accra Region'), ('\u2060Ashanti Region', '\u2060Ashanti Region'), ('Western Region', 'Western Region'), ('Western North Region', 'Western North Region'), ('Central Region', 'Central Region'), ('Eastern Region', 'Eastern Region'), ('\u2060Volta Region', '\u2060Volta Region'), ('Oti Region', 'Oti Region'), ('\u2060Northern Region', '\u2060Northern Region'), ('\u2060Savannah Region', '\u2060Savannah Region'), ('North East Region', 'North East Region'), ('Upper East Region', 'Upper East Region'), ('\u2060Upper West Region', '\u2060Upper West Region'), ('Bono Region', 'Bono Region'), ('Bono East Region', 'Bono East Region'), ('Ahafo Region', 'Ahafo Region')], max_length=100),
        ),
    ]
