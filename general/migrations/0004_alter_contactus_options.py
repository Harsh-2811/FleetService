# Generated by Django 4.2.16 on 2024-10-15 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0003_contactus_created_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contactus",
            options={"verbose_name_plural": "Contact Us"},
        ),
    ]