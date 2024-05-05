from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    verbose_name_plural = "Appointments"

    ordering = ["created_on"]
    list_display = (
        "appointment_id",
        "report_id",
        "client",
        "date",
        "time_slot",
        "session_type",
        "status",
        "consultant",
    )
    list_filter = ("date", "session_type", "status")
    search_fields = ("appointment_id", "student_email", "consultant_email")

    fieldsets = (
        (
            "Appointment General Information",
            {
                "fields": (
                    "appointment_id",
                    "report_id",
                    "status",
                    "session_type",
                    "date",
                    "start_time",
                    "end_time",
                    "time_slot",
                    "physical_location",
                ),
            },
        ),
        (
            "Student Information",
            {
                "fields": (
                    "client",
                    "student_full_name",
                    "student_email",
                    "student_phone",
                    "student_reg_no",
                    "student_gender",
                ),
            },
        ),
        (
            "Consultant Information",
            {
                "fields": (
                    "consultant",
                    "consultant_phone",
                    "consultant_office",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        # Define the fields you want to make read-only
        readonly_fields = (
            "appointment_id",
            "report_id",
            "client",
            "student_full_name",
            "student_email",
            "student_phone",
            "student_reg_no",
            "student_gender",
        )
        return readonly_fields + super().get_readonly_fields(request, obj)
