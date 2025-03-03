# Generated by Django 5.1.4 on 2025-01-08 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0003_delete_rental'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
