# Generated by Django 4.2.16 on 2024-10-10 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0006_vehicle_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='driver',
        ),
    ]
