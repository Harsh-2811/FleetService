# Generated by Django 4.2.16 on 2024-10-11 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_remove_job_job_time_job_job_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
