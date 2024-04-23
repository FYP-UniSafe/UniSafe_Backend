from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_id",
        "status",
        "abuse_type",
        "created_on",
        "assigned_gd",
        "reporter",
        "report_for",
    )
    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "report_id",
                    "status",
                    "assigned_gd",
                    "rejection_reason",
                    "report_for",
                )
            },
        ),
        (
            "Reporter Contact Details",
            {
                "fields": (
                    "reporter",
                    "reporter_email",
                    "reporter_phone",
                    "reporter_full_name",
                    "reporter_gender",
                    "reporter_reg_no",
                    "reporter_college",
                )
            },
        ),
        (
            "Victim Details",
            {
                "fields": (
                    "victim_email",
                    "victim_full_name",
                    "victim_phone",
                    "victim_gender",
                    "victim_reg_no",
                    "victim_college",
                )
            },
        ),
        (
            "Abuse Information",
            {
                "fields": (
                    "abuse_type",
                    "date_and_time",
                    "location",
                    "description",
                    # "evidence",
                )
            },
        ),
        (
            "Perpetrator Details",
            {"fields": ("perpetrator_fullname", "perpetrator_gender", "relationship")},
        ),
        ("Police Status", {"fields": ("police_status", "assigned_officer")}),
    )
    readonly_fields = (
        "report_id",
        "reporter",
        "rejection_reason",
        "assigned_gd",
        "reporter_email",
        "reporter_phone",
        "reporter_full_name",
        "reporter_gender",
        "reporter_reg_no",
        "reporter_college",
        "victim_email",
        "victim_full_name",
        "victim_phone",
        "victim_gender",
        "victim_reg_no",
        "victim_college",
        "abuse_type",
        "date_and_time",
        "location",
        "description",
        # "evidence",
        "perpetrator_fullname",
        "perpetrator_gender",
        "relationship",
        "report_for",
    )

    ordering = ("created_on",)


admin.site.register(Report, ReportAdmin)
