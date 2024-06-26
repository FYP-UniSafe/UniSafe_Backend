from django.db import models
from users_app.models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 262144000:  # 250 MB (250 * 1024 * 1024)
        raise ValidationError(_("The maximum file size that can be uploaded is 250MB"))


class Report(models.Model):
    REPORT_FOR_CHOICES = [("Self", "Self"), ("Else", "Else")]
    LOCATIONS_CHOICES = [
        ("Hall I", "Hall I"),
        ("Hall II", "Hall II"),
        ("Hall III", "Hall III"),
        ("Hall IV", "Hall IV"),
        ("Hall V", "Hall V"),
        ("Hall VI", "Hall VI"),
        ("Hall VII", "Hall VII"),
        ("Magufuli Hostels", "Magufuli Hostels"),
        ("Mabibo Hostels", "Mabibo Hostels"),
        ("Kunduchi Hostels", "Kunduchi Hostels"),
        ("CoICT Hostels", "CoICT Hostels"),
        ("Ubungo Hostels", "Ubungo Hostels"),
        ("Other", "Other"),
    ]
    ABUSE_TYPE_CHOICES = [
        ("Physical Violence", "Physical Violence"),
        ("Sexual Violence", "Sexual Violence"),
        ("Psychological Violence", "Psychological Violence"),
        ("Online Harassment", "Online Harassment"),
        ("Societal Violence", "Societal Violence"),
    ]

    report_for = models.CharField(max_length=10, choices=REPORT_FOR_CHOICES)
    report_id = models.CharField(primary_key=True, max_length=25, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, default="PENDING"
    )  # Pending, Rejected, In Progress, Forwarded to Police, Resolved.
    assigned_gd = models.ForeignKey(
        GenderDesk, on_delete=models.SET_NULL, null=True, blank=True, default=None
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
    # Victim's Details
    victim_email = models.EmailField()
    victim_full_name = models.CharField(max_length=255)
    victim_phone = models.CharField(max_length=20)
    victim_gender = models.CharField(max_length=20)
    victim_reg_no = models.CharField(max_length=255)
    victim_college = models.CharField(max_length=255)
    # Description of the Abuse
    abuse_type = models.CharField(max_length=50, choices=ABUSE_TYPE_CHOICES)
    date_and_time = models.DateTimeField()
    # location = models.TextField(max_length=20)
    location = models.CharField(max_length=20, choices=LOCATIONS_CHOICES)
    other_location = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField()
    # Perpetrator Details
    perpetrator_fullname = models.TextField(max_length=20, blank=True, null=True)
    perpetrator_gender = models.TextField(max_length=20)
    relationship = models.TextField(max_length=50)
    # Police Status
    police_status = models.CharField(max_length=20, default="UNFORWARDED")
    assigned_officer = models.ForeignKey(
        Police, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            total_reports = Report.objects.count() + 1
            self.report_id = f"RE{self.reporter_reg_no}-{total_reports}"

        super().save(*args, **kwargs)


class AnonymousReport(models.Model):
    LOCATIONS_CHOICES = [
        ("Hall I", "Hall I"),
        ("Hall II", "Hall II"),
        ("Hall III", "Hall III"),
        ("Hall IV", "Hall IV"),
        ("Hall V", "Hall V"),
        ("Hall VI", "Hall VI"),
        ("Hall VII", "Hall VII"),
        ("Magufuli Hostels", "Magufuli Hostels"),
        ("Mabibo Hostels", "Mabibo Hostels"),
        ("Kunduchi Hostels", "Kunduchi Hostels"),
        ("CoICT Hostels", "CoICT Hostels"),
        ("Ubungo Hostels", "Ubungo Hostels"),
        ("Other", "Other"),
    ]
    ABUSE_TYPE_CHOICES = [
        ("Physical Violence", "Physical Violence"),
        ("Sexual Violence", "Sexual Violence"),
        ("Psychological Violence", "Psychological Violence"),
        ("Online Harassment", "Online Harassment"),
        ("Societal Violence", "Societal Violence"),
    ]
    report_id = models.CharField(primary_key=True, max_length=25, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="PENDING")
    assigned_gd = models.ForeignKey(
        GenderDesk, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    rejection_reason = models.TextField(
        max_length=255, blank=True, null=True, default=None
    )
    reporter_phone = models.CharField(max_length=20, null=True, blank=True)
    # Description of the Abuse
    abuse_type = models.CharField(max_length=50, choices=ABUSE_TYPE_CHOICES)
    date_and_time = models.DateTimeField()
    # location = models.TextField(max_length=20)
    location = models.CharField(max_length=20, choices=LOCATIONS_CHOICES)
    other_location = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField()
    # Perpetrator Details
    perpetrator_fullname = models.TextField(max_length=20, blank=True, null=True)
    perpetrator_gender = models.TextField(max_length=20)
    relationship = models.TextField(max_length=20)
    # Police Status
    police_status = models.CharField(max_length=20, default="UNFORWARDED")
    assigned_officer = models.ForeignKey(
        Police, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            total_reports = AnonymousReport.objects.count() + 1
            self.report_id = f"A-RE-{total_reports}"
        super().save(*args, **kwargs)


class Evidence(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.DO_NOTHING,
        blank=True,
        related_name="report_evidence",
    )
    evidence = models.FileField(upload_to="assets/evidence/", blank=True, null=True, validators=[validate_file_size])


class AnonymousEvidence(models.Model):
    report = models.ForeignKey(
        AnonymousReport,
        on_delete=models.DO_NOTHING,
        blank=True,
        related_name="anonymous_evidence",
    )
    evidence = models.FileField(upload_to="assets/evidence/", blank=True, null=True, validators=[validate_file_size])
