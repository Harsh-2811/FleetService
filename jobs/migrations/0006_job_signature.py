# Generated by Django 4.2.16 on 2024-10-17 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_prefillchecks_check_type_precheckimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/'),
        ),
    ]