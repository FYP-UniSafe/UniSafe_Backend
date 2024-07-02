from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class CreateAppointmentSerializer(serializers.ModelSerializer):
    appointment_id = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        exclude = [
            "report_id",
            "consultant",
            "consultant_phone",
            "consultant_office",
            "client",
            "start_time",
            "end_time",
            "time_slot",
            "physical_location",
        ]


class AcceptAppointmentSerializer(serializers.ModelSerializer):
    appointment_id = serializers.CharField(read_only=True)
    meeting_id = serializers.CharField(read_only=True)  # Include meeting_id

    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "meeting_token",
            "meeting_id",
            "physical_location",
            "start_time",
            "end_time",
        ]

    def validate(self, attrs):
        session_type = (
            self.instance.session_type if self.instance else attrs.get("session_type")
        )
        physical_location = attrs.get("physical_location")

        if session_type == "Online":
            attrs.pop("physical_location", None)
        elif session_type == "Physical":
            attrs.pop("meeting_id", "meeting_token", None)

            if not physical_location:
                raise serializers.ValidationError(
                    "physical_location is required for Physical appointments."
                )

        if not attrs.get("start_time"):
            raise serializers.ValidationError("start_time is required.")

        if not attrs.get("end_time"):
            raise serializers.ValidationError("end_time is required.")

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        session_type = instance.session_type

        if session_type == "Online" and "physical_location" in representation:
            del representation["physical_location"]
        elif session_type == "Physical" and "meeting_id" in representation:
            del representation["meeting_id"]

        return representation
