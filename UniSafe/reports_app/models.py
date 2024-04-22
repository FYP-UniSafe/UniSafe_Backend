from django.db import models
from users_app.models import *


class Report(models.Model):
    REPORT_FOR_CHOICES = [("Self", "Self"), ("Else", "Else")]

    report_id = models.CharField(primary_key=True, max_length=25, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, default="PENDING"
    )  # Pending, Rejected, In Progress, Forwarded to Police, Resolved.
    assigned_gd = models.ForeignKey(
        GenderDesk, on_delete=models.DO_NOTHING, null=True, blank=True, default=None
    )
    rejection_reason = models.TextField(
        max_length=255, blank=True, null=True, default=None
    )

    # Reporter Contact Details
    reporter = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name="reported_cases"
    )
    reporter_full_name = models.CharField(max_length=255)
    reporter_gender = models.CharField(max_length=6)
    reporter_college = models.CharField(max_length=255)
    reporter_reg_no = models.CharField(max_length=255)
    reporter_email = models.EmailField()
    reporter_phone = models.CharField(max_length=20)

    report_for = models.CharField(max_length=10, choices=REPORT_FOR_CHOICES)

    # Victim's Details
    victim_email = models.EmailField()
    victim_full_name = models.CharField(max_length=255)
    victim_phone = models.CharField(max_length=20)
    victim_gender = models.CharField(max_length=6)
    victim_reg_no = models.CharField(max_length=255)
    victim_college = models.CharField(max_length=255)

    # Description of the Abuse
    abuse_type = models.TextField(max_length=20)
    date_and_time = models.DateTimeField()
    location = models.TextField(max_length=20)
    description = models.TextField()
    evidence = models.FileField(upload_to="assets/evidence/", blank=True, null=True)

    # Perpetrator Details
    perpetrator_fullname = models.TextField(max_length=20)
    perpetrator_gender = models.TextField(max_length=20)
    relationship = models.TextField(max_length=20)

    # Police Status
    police_status = models.CharField(max_length=20, default="UNFORWARDED")
    assigned_officer = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, null=True, blank=True, default=None
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            total_reports = Report.objects.count() + 1
            self.report_id = f"RE{self.reporter_reg_no}-{total_reports}"

        super().save(*args, **kwargs)


class AnonymousReport(models.Model):
    report_id = models.CharField(primary_key=True, max_length=25, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="PENDING")
    assigned_gd = models.ForeignKey(
        GenderDesk, on_delete=models.DO_NOTHING, null=True, blank=True, default=None
    )

    # Description of the Abuse
    abuse_type = models.TextField(max_length=20)
    date_and_time = models.DateTimeField()
    location = models.TextField(max_length=20)
    description = models.TextField()
    evidence = models.FileField(upload_to="assets/evidence/", blank=True, null=True)

    # Perpetrator Details
    perpetrator_fullname = models.TextField(max_length=20)
    perpetrator_gender = models.TextField(max_length=20)
    relationship = models.TextField(max_length=20)

    # Police Status
    police_status = models.CharField(max_length=20, default="UNFORWARDED")
    assigned_officer = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, null=True, blank=True, default=None
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            total_reports = AnonymousReport.objects.count() + 1
            self.report_id = f"AR{total_reports}"
        super().save(*args, **kwargs)
