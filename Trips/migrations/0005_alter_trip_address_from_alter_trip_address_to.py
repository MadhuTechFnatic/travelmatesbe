# Generated by Django 5.0.3 on 2024-03-05 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trips', '0004_trip_time_alter_trip_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='address_from',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trip',
            name='address_to',
            field=models.CharField(max_length=100),
        ),
    ]