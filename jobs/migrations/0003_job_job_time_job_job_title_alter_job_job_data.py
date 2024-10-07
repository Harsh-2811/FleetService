# Generated by Django 4.2.16 on 2024-10-07 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_data',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]