from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['status', 'assigned_gd', 'report_for', 'victim_email', 'victim_full_name', 'victim_phone', 'victim_gender', 'victim_reg_no', 'victim_college', 'abuse_type', 'date_and_time', 'location', 'description', 'evidence', 'perpetrator_fullname', 'perpetrator_gender', 'relationship', 'police_status', 'assigned_officer']


class ReportListSerializer(serializers.ModelSerializer):
    # reporter = serializers.CharField(source='reporter_full_name')
    # assigned_gd = serializers.CharField(source='assigned_gd.user')
    # # police_status = serializers.CharField(source='police_status')
    # assigned_officer = serializers.CharField(source='assigned_officer.user')

    class Meta:
        model = Report
        fields = ['id', 'status', 'reporter', 'created_on', 'assigned_gd', 'police_status', 'assigned_officer']