# Generated by Django 4.2.16 on 2024-10-12 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="JobFormField",
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
                ("field_name", models.CharField(max_length=100)),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("Text", "Text"),
                            ("Number", "Number"),
                            ("Boolean", "Boolean"),
                            ("Select", "Select"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SelectOption",
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
                ("option_value", models.CharField(max_length=100)),
                (
                    "job_form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="select_options",
                        to="general.jobformfield",
                    ),
                ),
            ],
        ),
    ]
