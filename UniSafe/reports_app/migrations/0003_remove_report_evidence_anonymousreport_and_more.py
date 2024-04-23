# Generated by Django 5.0.1 on 2024-04-23 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports_app", "0002_initial"),
        ("users_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="report",
            name="evidence",
        ),
        migrations.CreateModel(
            name="AnonymousReport",
            fields=[
                (
                    "report_id",
                    models.CharField(
                        max_length=25, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="PENDING", max_length=20)),
                ("abuse_type", models.TextField(max_length=20)),
                ("date_and_time", models.DateTimeField()),
                ("location", models.TextField(max_length=20)),
                ("description", models.TextField()),
                ("perpetrator_fullname", models.TextField(max_length=20)),
                ("perpetrator_gender", models.TextField(max_length=20)),
                ("relationship", models.TextField(max_length=20)),
                (
                    "police_status",
                    models.CharField(default="UNFORWARDED", max_length=20),
                ),
                (
                    "assigned_gd",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="users_app.genderdesk",
                    ),
                ),
                (
                    "assigned_officer",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="users_app.police",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AnonymousEvidence",
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
                (
                    "evidence",
                    models.FileField(
                        blank=True, null=True, upload_to="assets/evidence/"
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="anonymous_evidence",
                        to="reports_app.anonymousreport",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Evidence",
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
                (
                    "evidence",
                    models.FileField(
                        blank=True, null=True, upload_to="assets/evidence/"
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="report_evidence",
                        to="reports_app.report",
                    ),
                ),
            ],
        ),
    ]
