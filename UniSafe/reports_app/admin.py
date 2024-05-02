from django.contrib import admin
from .models import Report, AnonymousReport, Evidence, AnonymousEvidence


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1


class AnonymousEvidenceInline(admin.TabularInline):
    model = AnonymousEvidence
    extra = 1


class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "evidence")
    list_filter = ("report",)
    search_fields = ["report_id", "report__report_id", "evidence"]


class AnonymousEvidenceAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "evidence")
    list_filter = ("report",)
    search_fields = ["report_id", "report__report_id", "evidence"]


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
                    "created_on",
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
                    "other_location",
                    "description",
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
        "created_on",
        "reporter",
        "rejection_reason",
        # "assigned_gd",
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
        "other_location",
        "description",
        "perpetrator_fullname",
        "perpetrator_gender",
        "relationship",
        "report_for",
    )

    ordering = ("created_on",)
    inlines = [EvidenceInline]


class AnonymousReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_id",
        "status",
        "rejection_reason",
        "abuse_type",
        "created_on",
        "assigned_gd",
        "police_status",
        "assigned_officer",
    )
    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "report_id",
                    "created_on",
                    "status",
                    "assigned_gd",
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
                    "other_location",
                    "description",
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
        "status",
        "report_id",
        "created_on",
        # "assigned_gd",
        "abuse_type",
        "date_and_time",
        "location",
        "other_location",
        "description",
        "perpetrator_fullname",
        "perpetrator_gender",
        "relationship",
        "police_status",
        # "assigned_officer",
    )

    ordering = ("created_on",)
    inlines = [AnonymousEvidenceInline]


admin.site.register(Report, ReportAdmin)
admin.site.register(AnonymousReport, AnonymousReportAdmin)
admin.site.register(Evidence, EvidenceAdmin)
admin.site.register(AnonymousEvidence, AnonymousEvidenceAdmin)
