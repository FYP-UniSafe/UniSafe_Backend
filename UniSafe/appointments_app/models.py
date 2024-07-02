from django.db import models
from reports_app.models import *
from users_app.models import *


class Appointment(models.Model):
    SESSION_TYPE_CHOICES = [("Physical", "Physical"), ("Online", "Online")]
    APPOINTMENT_STATUS_CHOICES = [
        ("REQUESTED", "REQUESTED"),
        ("SCHEDULED", "SCHEDULED"),
        ("CLOSED", "CLOSED"),
        ("CANCELLED", "CANCELLED"),
        ("MISSED", "MISSED")
    ]

    # Appointment general information
    appointment_id = models.CharField(primary_key=True, max_length=25, unique=True)
    report_id = models.ForeignKey(
        Report,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=APPOINTMENT_STATUS_CHOICES, default='REQUESTED')
    session_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(null=True, blank=True, default=None)
    end_time = models.TimeField(null=True, blank=True, default=None)
    time_slot = models.CharField(max_length=13, null=True, blank=True, default=None)
    physical_location = models.CharField(max_length=25, blank=True, default=None, null=True)
    meeting_id = models.CharField(max_length=255, null=True, blank=True)
    meeting_token = models.TextField(null=True, blank=True)

    # Student information
    client = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        related_name="appointments_created",
        null=False,
        blank=False,
    )
    student_full_name = models.CharField(max_length=50)
    student_email = models.EmailField()
    student_phone = models.CharField(max_length=15)
    student_reg_no = models.CharField(max_length=20)
    student_gender = models.CharField(max_length=6)

    # Consultant information
    consultant = models.ForeignKey(
        Consultant,
        on_delete=models.DO_NOTHING,
        related_name="scheduled_appointments",
        default=None,
        null=True,
        blank=True,
    )
    consultant_phone = models.CharField(max_length=15)
    consultant_office = models.CharField(max_length=20)

    def __str__(self):
        return self.appointment_id

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.time_slot = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        if not self.pk:
            total_appointments = Appointment.objects.count()
            self.appointment_id = f"AP{self.student_reg_no}-{total_appointments+1}"
        super().save(*args, **kwargs)