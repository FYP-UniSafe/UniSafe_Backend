from rest_framework import serializers
from .models import Report, AnonymousReport


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class CreateReportSerializer(serializers.ModelSerializer):
    report_id = serializers.CharField(read_only=True)
    reporter = serializers.CharField(read_only=True)
    reporter_full_name = serializers.CharField(read_only=True)
    reporter_gender = serializers.CharField(read_only=True)
    reporter_college = serializers.CharField(read_only=True)
    reporter_reg_no = serializers.CharField(read_only=True)
    reporter_email = serializers.CharField(read_only=True)
    reporter_phone = serializers.CharField(read_only=True)

    victim_email = serializers.EmailField(read_only=True)
    victim_full_name = serializers.CharField(read_only=True)
    victim_phone = serializers.CharField(read_only=True)
    victim_gender = serializers.CharField(read_only=True)
    victim_reg_no = serializers.CharField(read_only=True)
    victim_college = serializers.CharField(read_only=True)

    class Meta:
        model = Report
        fields = [
            "report_id",
            "status",
            "assigned_gd",
            "reporter",
            "reporter_full_name",
            "reporter_gender",
            "reporter_college",
            "reporter_reg_no",
            "reporter_email",
            "reporter_phone",
            "report_for",
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
            "evidence",
            "perpetrator_fullname",
            "perpetrator_gender",
            "relationship",
            "police_status",
            "assigned_officer",
        ]


class ReportListSerializer(serializers.ModelSerializer):
    # reporter = serializers.CharField(source='reporter_full_name')
    # assigned_gd = serializers.CharField(source='assigned_gd.user')
    # # police_status = serializers.CharField(source='police_status')
    # assigned_officer = serializers.CharField(source='assigned_officer.user')

    class Meta:
        model = Report
        fields = [
            "report_id",
            "status",
            "reporter",
            "created_on",
            "assigned_gd",
            "police_status",
            "assigned_officer",
        ]


class AcceptReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class RejectReportSerializer(serializers.ModelSerializer):
    report_id = serializers.CharField(required=True)
    rejection_reason = serializers.CharField(required=True)

    class Meta:
        model = Report
        fields = ["report_id", "status", "rejection_reason"]


class ForwardReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class ReceiveReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class CloseReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class ListAllReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "report_id",
            "status",
            "assigned_gd",
            "reporter",
            "reporter_full_name",
            "reporter_gender",
            "reporter_college",
            "reporter_reg_no",
            "reporter_email",
            "reporter_phone",
            "report_for",
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
            "evidence",
            "perpetrator_fullname",
            "perpetrator_gender",
            "relationship",
            "police_status",
            "assigned_officer",
        ]


class StudentReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class AssignedReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ForwardedReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'




#ANONYMOUS REPORT
class AnonymousReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousReport
        fields = "__all__"

class CreateAnonymousReportSerializer(serializers.ModelSerializer):
    report_id = serializers.CharField(read_only=True)

    class Meta:
        model = AnonymousReport
        fields = [
            "report_id",
            "status",
            "assigned_gd",
            "abuse_type",
            "date_and_time",
            "location",
            "description",
            "evidence",
            "perpetrator_fullname",
            "perpetrator_gender",
            "relationship",
            "police_status",
            "assigned_officer",
        ]

class AnonymousReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousReport
        fields = [
            "report_id",
            "status",
            "created_on",
            "assigned_gd",
            "police_status",
            "assigned_officer",
        ]