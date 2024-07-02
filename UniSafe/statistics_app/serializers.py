from rest_framework import serializers

class ReportCountsSerializer(serializers.Serializer):
    report_count = serializers.IntegerField()
    anonymous_report_count = serializers.IntegerField()

class ReportsPerCaseTypeSerializer(serializers.Serializer):
    abuse_type = serializers.CharField()
    count = serializers.IntegerField()

class ReportsPerYearSerializer(serializers.Serializer):
    year = serializers.CharField()
    count = serializers.IntegerField()

class ReportsPerLocationSerializer(serializers.Serializer):
    center = serializers.DictField(child=serializers.FloatField())
    cases = serializers.IntegerField()

class AuxiliaryPoliceLocationsSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
