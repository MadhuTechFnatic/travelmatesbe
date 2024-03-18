# Generated by Django 5.0.3 on 2024-03-17 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_userstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstatus',
            name='status',
        ),
        migrations.AddField(
            model_name='userstatus',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]