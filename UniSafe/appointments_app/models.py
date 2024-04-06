from django.db import models
from reports_app.models import *
from users_app.models import *


class Appointment(models.Model):
    SESSION_TYPE_CHOICES = [("Physical", "Physical"), ("Online", "Online")]

    # Appointment general information
    appointment_id = models.CharField(primary_key=True, max_length=25, unique=True)
    report_id = models.ForeignKey(
        Report,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None,
    )
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(null=True, blank=True, default=None)
    session_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES)

    # Student information
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name="scheduled_appointments"
    )
    student_full_name = models.CharField(max_length=100)
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
        if not self.pk:
            total_appointments = Appointment.objects.count()
            self.appointment_id = f"AP{self.student_reg_no}-{total_appointments+1}"

        super().save(*args, **kwargs)
