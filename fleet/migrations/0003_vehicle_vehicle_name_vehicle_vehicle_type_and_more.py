# Generated by Django 4.2.16 on 2024-10-03 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet', '0002_driver_driver_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(blank=True, choices=[('flatbed_truck', 'Flatbed Trucks'), ('number', 'Tail-Lift Trucks'), ('box_trucks', 'Box Trucks'), ('dump_trucks', 'Dump Trucks'), ('semi_trailer_trucks', 'Semi-Trailer Trucks'), ('jumbo_trailer_trucks', 'Jumbo Trailer Trucks'), ('tanker_trucks', 'Tanker Trucks'), ('refrigerated_trucks', 'Refrigerated Trucks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='fleet.driver'),
        ),
    ]
