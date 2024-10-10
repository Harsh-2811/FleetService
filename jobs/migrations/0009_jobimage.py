# Generated by Django 4.2.16 on 2024-10-08 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_job_job_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('arrive_job', 'Arrive Job'), ('arrive_site', 'Arrive Site')], max_length=11)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_image', to='jobs.job')),
            ],
        ),
    ]
