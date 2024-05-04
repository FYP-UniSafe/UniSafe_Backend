from rest_framework import serializers
from .models import Report, AnonymousReport


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "report_id",
            "status",
            "report_for",
            "abuse_type",
            "date_and_time",
            "location",
            "other_location",
            "description",
            "perpetrator_fullname",
            "perpetrator_gender",
            "relationship",
            "victim_email",
            "victim_full_name",
            "victim_phone",
            "victim_gender",
            "victim_reg_no",
            "victim_college",
        ]
        read_only_fields = [
            "report_id",
            "status",
        ]
        extra_kwargs = {
            "victim_email": {"required": False},
            "victim_full_name": {"required": False},
            "victim_phone": {"required": False},
            "victim_gender": {"required": False},
            "victim_reg_no": {"required": False},
            "victim_college": {"required": False},
        }

    def validate(self, data):
        report_for = data.get("report_for")

        # Required fields regardless of report_for
        required_fields = [
            "abuse_type",
            "date_and_time",
            "location",
            "description",
            "perpetrator_gender",
            "relationship",
        ]

        if report_for == "Else":
            required_fields = [
                "victim_email",
                "victim_full_name",
                "victim_phone",
                "victim_gender",
                "victim_reg_no",
                "victim_college",
            ]

            missing_fields = []

            for field in required_fields:
                if not data.get(field):
                    missing_fields.append(field)

            if missing_fields:
                error_messages = {
                    field: [f"This field is required"] for field in missing_fields
                }
                raise serializers.ValidationError(error_messages)
        elif report_for == "Self":
            # Populate victim details using user's data
            user = self.context["request"].user
            profile = user.profile

            data["victim_email"] = user.email
            data["victim_full_name"] = user.full_name
            data["victim_phone"] = user.phone_number
            data["victim_gender"] = user.gender
            data["victim_reg_no"] = profile.reg_no
            data["victim_college"] = profile.college

        return data

    def validate_location(self, value):
        if value == "Other":
            if not self.initial_data.get("other_location"):
                raise serializers.ValidationError(
                    "Please provide a value for other_location field."
                )
        return value

    def create(self, validated_data):
        if validated_data["location"] == "Other":
            validated_data["other_location"] = self.initial_data.get(
                "other_location", ""
            )
        return super().create(validated_data)


class ReportListSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source="reporter_full_name")
    assigned_gd = serializers.CharField(source="assigned_gd.user")
    assigned_officer = serializers.CharField(source="assigned_officer.user")

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
    evidence = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Report
        fields = "__all__"


class StudentReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class AssignedReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class ForwardedReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


# ANONYMOUS REPORT
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
            "other_location",
            "description",
            "perpetrator_fullname",
            "perpetrator_gender",
            "relationship",
            "police_status",
            "assigned_officer",
        ]
        read_only_fields = [
            "status",
            "report_id",
            "assigned_gd",
            "police_status",
            "assigned_officer",
        ]

    def validate_location(self, value):
        if value == "Other":
            if not self.initial_data.get("other_location"):
                raise serializers.ValidationError(
                    "Please provide a value for other_location."
                )
        return value

    def create(self, validated_data):
        if validated_data["location"] == "Other":
            validated_data["other_location"] = self.initial_data.get(
                "other_location", ""
            )
        return super().create(validated_data)


class AnonymousReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousReport
        fields = "__all__"


class AcceptAnonymousReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class RejectAnonymousReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)
    rejection_reason = serializers.CharField(required=True)

    class Meta:
        model = AnonymousReport
        fields = ["report_id", "status", "rejection_reason"]


class AssignedAnonymousReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousReport
        fields = "__all__"


class ForwardAnonymousReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class ReceiveAnonymousReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class CloseAnonymousReportSerializer(serializers.Serializer):
    report_id = serializers.CharField(required=True)


class ForwardedAnonymousReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousReport
        fields = "__all__"
