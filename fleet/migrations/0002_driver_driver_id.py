# Generated by Django 4.2.16 on 2024-10-02 06:55

from django.db import migrations, models
import fleet.models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driver_id',
            field=models.CharField(default=fleet.models.generate_driver_id, editable=False, max_length=10, unique=True),
        ),
    ]
