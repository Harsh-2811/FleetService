# Generated by Django 4.2.16 on 2024-10-03 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fleet', '0004_alter_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_data', models.TextField(max_length=200)),
                ('job_status', models.CharField(choices=[('Assigned', 'Assigned'), ('Running', 'Running'), ('Finished', 'Finished'), ('Break', 'Break')], default='Assigned', max_length=10)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('break_start', models.DateTimeField(blank=True, null=True)),
                ('break_end', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='fleet.driver')),
            ],
        ),
    ]
