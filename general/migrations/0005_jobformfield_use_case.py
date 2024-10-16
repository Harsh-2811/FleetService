# Generated by Django 4.2.16 on 2024-10-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_alter_contactus_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobformfield',
            name='use_case',
            field=models.CharField(choices=[('Start Day', 'Start Day'), ('Finish Job', 'Finish Job'), ('Finish Day', 'Finish Day')], default='Start Day', max_length=50),
        ),
    ]
