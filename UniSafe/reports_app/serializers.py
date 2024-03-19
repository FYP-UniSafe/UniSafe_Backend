from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ReportListSerializer(serializers.ModelSerializer):
    # reporter = serializers.CharField(source='reporter_full_name')
    # assigned_gd = serializers.CharField(source='assigned_gd.user')
    # # police_status = serializers.CharField(source='police_status')
    # assigned_officer = serializers.CharField(source='assigned_officer.user')

    class Meta:
        model = Report
        fields = ['id', 'status', 'reporter', 'created_on', 'assigned_gd', 'police_status', 'assigned_officer']