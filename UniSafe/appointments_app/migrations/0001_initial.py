# Generated by Django 5.0.1 on 2024-05-05 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "appointment_id",
                    models.CharField(
                        max_length=25, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("REQUESTED", "REQUESTED"),
                            ("SCHEDULED", "SCHEDULED"),
                            ("CLOSED", "CLOSED"),
                        ],
                        default="REQUESTED",
                        max_length=15,
                    ),
                ),
                (
                    "session_type",
                    models.CharField(
                        choices=[("Physical", "Physical"), ("Online", "Online")],
                        max_length=10,
                    ),
                ),
                ("date", models.DateField()),
                ("start_time", models.TimeField(blank=True, default=None, null=True)),
                ("end_time", models.TimeField(blank=True, default=None, null=True)),
                (
                    "time_slot",
                    models.CharField(
                        blank=True, default=None, max_length=13, null=True
                    ),
                ),
                (
                    "physical_location",
                    models.CharField(
                        blank=True, default=None, max_length=25, null=True
                    ),
                ),
                ("student_full_name", models.CharField(max_length=50)),
                ("student_email", models.EmailField(max_length=254)),
                ("student_phone", models.CharField(max_length=15)),
                ("student_reg_no", models.CharField(max_length=20)),
                ("student_gender", models.CharField(max_length=6)),
                ("consultant_phone", models.CharField(max_length=15)),
                ("consultant_office", models.CharField(max_length=20)),
            ],
        ),
    ]
