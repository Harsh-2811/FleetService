# Generated by Django 4.2.16 on 2024-10-07 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_job_time_job_job_title_alter_job_job_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]