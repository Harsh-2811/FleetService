# Generated by Django 4.2.16 on 2024-10-17 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fleet", "0003_alter_driver_user"),
        ("jobs", "0004_prefillchecks"),
    ]

    operations = [
        migrations.AddField(
            model_name="prefillchecks",
            name="check_type",
            field=models.CharField(
                choices=[("start_day", "Start Day"), ("finish_day", "Finish Day")],
                default="start_day",
                max_length=50,
            ),
        ),
        migrations.CreateModel(
            name="PrecheckImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="day_images",
                        to="fleet.driver",
                    ),
                ),
            ],
        ),
    ]