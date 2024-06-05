from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework import generics
from rest_framework.response import Response
from reports_app.models import Report, AnonymousReport


class ReportCountsView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        report_count = Report.objects.filter(~Q(status="REJECTED")).count()
        anonymous_report_count = AnonymousReport.objects.filter(
            ~Q(status="REJECTED")
        ).count()

        response_data = {
            "report_count": report_count,
            "anonymous_report_count": anonymous_report_count,
        }

        return Response(response_data)


class ReportsPerCaseTypeView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        report_case_type_data = (
            Report.objects.exclude(status="REJECTED")
            .values("abuse_type")
            .annotate(count=Count("abuse_type"))
        )
        anonymous_report_case_type_data = (
            AnonymousReport.objects.exclude(status="REJECTED")
            .values("abuse_type")
            .annotate(count=Count("abuse_type"))
        )

        combined_data = {}
        for data in report_case_type_data:
            combined_data[data["abuse_type"]] = (
                combined_data.get(data["abuse_type"], 0) + data["count"]
            )
        for data in anonymous_report_case_type_data:
            combined_data[data["abuse_type"]] = (
                combined_data.get(data["abuse_type"], 0) + data["count"]
            )

        response_data = [
            {"abuse_type": abuse_type, "count": count}
            for abuse_type, count in combined_data.items()
        ]

        return Response(response_data)


# THIS WILL BE USED ONCE THE SYSTEM IS COMPLETE
# class ReportsPerYearView(generics.ListAPIView):

#     def get(self, request, *args, **kwargs):
#         current_year = timezone.now().year
#         response_data = []

#         for year in range(current_year, current_year + 5):
#             start_date = timezone.make_aware(datetime(year, 8, 1))
#             end_date = timezone.make_aware(datetime(year + 1, 7, 31))

#             report_count = Report.objects.filter(
#                 Q(created_on__range=(start_date, end_date)) & ~Q(status="REJECTED")
#             ).count()

#             anonymous_report_count = AnonymousReport.objects.filter(
#                 Q(created_on__range=(start_date, end_date)) & ~Q(status="REJECTED")
#             ).count()

#             response_data.append({
#                 "year": f"{year}-{year+1}",
#                 "count": report_count + anonymous_report_count
#             })


#         return Response(response_data)
class ReportsPerYearView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        response_data = []

        for year in range(2023, 2023 + 5):
            start_date = timezone.make_aware(datetime(year, 8, 1))
            end_date = timezone.make_aware(datetime(year + 1, 7, 31))

            report_count = Report.objects.filter(
                Q(created_on__range=(start_date, end_date)) & ~Q(status="REJECTED")
            ).count()

            anonymous_report_count = AnonymousReport.objects.filter(
                Q(created_on__range=(start_date, end_date)) & ~Q(status="REJECTED")
            ).count()

            response_data.append(
                {
                    "year": f"{year}-{year+1}",
                    "count": report_count + anonymous_report_count,
                }
            )

        return Response(response_data)


class ReportsPerLocationView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        locations = {
            "Hall I": {
                "center": {"lat": -6.777830275857019, "lng": 39.20674868360372},
                "cases": 0,
            },
            "Hall II": {
                "center": {"lat": -6.776433326520683, "lng": 39.20761758999947},
                "cases": 0,
            },
            "Hall III": {
                "center": {"lat": -6.775460021509301, "lng": 39.206156004132886},
                "cases": 0,
            },
            "Hall IV": {
                "center": {"lat": -6.776342493802564, "lng": 39.205924524550916},
                "cases": 0,
            },
            "Hall V": {
                "center": {"lat": -6.776252280774953, "lng": 39.20715725250724},
                "cases": 0,
            },
            "Hall VI": {
                "center": {"lat": -6.775709422827955, "lng": 39.202819099746364},
                "cases": 0,
            },
            "Hall VII": {
                "center": {"lat": -6.7773403337781986, "lng": 39.20301746116488},
                "cases": 0,
            },
            "Magufuli Hostels": {
                "center": {"lat": -6.781932907748147, "lng": 39.21320137083932},
                "cases": 0,
            },
            "Mabibo Hostels": {
                "center": {"lat": -6.804887157350432, "lng": 39.20856607018921},
                "cases": 0,
            },
            "Kunduchi Hostels": {
                "center": {"lat": -6.6641503479942354, "lng": 39.216198491764985},
                "cases": 0,
            },
            "CoICT Hostels": {
                "center": {"lat": -6.772251650594132, "lng": 39.241099878854385},
                "cases": 0,
            },
            "Ubungo Hostels": {
                "center": {"lat": -6.792457483174008, "lng": 39.21243123112793},
                "cases": 0,
            },
            "Other": {"center": {"lat": 0, "lng": 0}, "cases": 0},
        }

        for location in locations:
            report_count = Report.objects.filter(
                ~Q(status="REJECTED"), location=location
            ).count()
            anonymous_report_count = AnonymousReport.objects.filter(
                ~Q(status="REJECTED"), location=location
            ).count()
            locations[location]["cases"] = report_count + anonymous_report_count

        return Response(locations)
