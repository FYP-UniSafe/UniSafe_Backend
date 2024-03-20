from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from users_app.models import *
from rest_framework.permissions import AllowAny, IsAuthenticated


class CreateReportView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = CreateReportSerializer

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        student_instance, _ = Student.objects.get_or_create(user=user)

        if not user.is_student:
            return Response(
                {"error": "Only students are allowed to create reports"},
                status=status.HTTP_403_FORBIDDEN,
            )

        reporter_data = {
            "reporter": student_instance,
            "reporter_full_name": user.full_name,
            "reporter_gender": user.gender,
            "reporter_email": user.email,
            "reporter_phone": user.phone_number,
            "reporter_college": profile.college,
            "reporter_reg_no": profile.reg_no,
        }

        serializer_data = serializer.validated_data
        serializer_data.update(reporter_data)

        serializer.save(**serializer_data)

        profile.report_count += 1
        profile.save()

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AcceptReportView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AcceptReportSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        user = request.user
        genderdesk_instance, _ = GenderDesk.objects.get_or_create(user=user)

        if not user.is_genderdesk:
            return Response(
                {
                    "error": "Only GenderDesk personnel are allowed to accept the reports"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if serializer.is_valid():
            report_id = serializer.validated_data["report_id"]

            if not report_id:
                return Response(
                    {"error": "Report ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                report = Report.objects.get(report_id=report_id)
            except Report.DoesNotExist:
                return Response(
                    {"error": "Report does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if report.status == "IN PROGRESS":
                response_data = {
                    "error": "The report has already been accepted by GenderDesk member {}.".format(
                        report.assigned_gd
                    ),
                    "status": report.status,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if report.status in ["REJECTED", "FORWARDED TO POLICE", "RESOLVED"]:
                return Response(
                    {"error": "Only pending reports can be accepted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            report.status = "IN PROGRESS"
            report.assigned_gd = genderdesk_instance
            report.rejection_reason = None
            report.save()

            response_data = {
                "message": "Report accepted successfully.",
                "status": report.status,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectReportView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = RejectReportSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        genderdesk_instance, _ = GenderDesk.objects.get_or_create(user=user)

        if not user.is_genderdesk:
            return Response(
                {
                    "error": "Only GenderDesk personnel are allowed to forward reports to the police"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        report_id = request.data.get("report_id")

        if not report_id:
            return Response(
                {"error": "Report ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            report = Report.objects.get(report_id=report_id)
        except Report.DoesNotExist:
            return Response(
                {"error": "Report does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if report.status == "REJECTED":
            return Response(
                {"error": "The report has already been rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if report.status in ["FORWARDED TO POLICE", "RESOLVED"]:
            return Response(
                {"error": "Only pending reports can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the report is already accepted by another GenderDesk personnel
        # One can reject if it was initially accepted by themselves
        if report.status == "ACCEPTED" and report.assigned_gd != genderdesk_instance:
            return Response(
                {
                    "error": "Cannot reject a report accepted by another GenderDesk member."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Initialize the serializer with the retrieved report instance
        serializer = self.get_serializer(report, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Ensure that the rejection_reason is provided
        if "rejection_reason" not in serializer.validated_data:
            return Response(
                {"error": "Rejection reason is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Before changing the status, check status is report is new, then this reject counts as a report handled.
        if report.status == "PENDING":
            profile.report_count += 1
            profile.save()

        serializer.validated_data["status"] = "REJECTED"
        serializer.save()

        report.assigned_gd = genderdesk_instance
        report.save()

        response_data = {
            "message": "Report rejected successfully.",
            "rejection_reason": report.rejection_reason,
            "status": report.status,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ForwardReportView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ForwardReportSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        genderdesk_instance, _ = GenderDesk.objects.get_or_create(user=user)

        if not user.is_genderdesk:
            return Response(
                {
                    "error": "Only GenderDesk personnel are allowed to forward reports to the police"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        report_id = serializer.validated_data["report_id"]

        try:
            report = Report.objects.get(report_id=report_id)
        except Report.DoesNotExist:
            return Response(
                {"error": "Report does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if report.police_status == "FORWARDED":
            return Response(
                {"error": "Report has already been forwarded to the police."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if report.status in ["REJECTED", "PENDING" "RESOLVED"]:
            return Response(
                {"error": "Report must be in progress to be forwarded to the police."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if report.assigned_gd != genderdesk_instance:
            return Response(
                {
                    "error": "Only the GenderDesk member who initially accepted the report can forward it to the police."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        report.police_status = "FORWARDED"
        report.status = "FORWARDED TO POLICE"
        report.save()

        return Response(
            {
                "message": "Report forwarded to the police successfully.",
                "status": report.status,
                "police_status": report.police_status,
            },
            status=status.HTTP_200_OK,
        )


class ReceiveReportView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReceiveReportSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        police_instance, _ = Police.objects.get_or_create(user=user)

        if not user.is_police:
            return Response(
                {"error": "Only police personnel are allowed to receive reports."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if serializer.is_valid():
            report_id = serializer.validated_data["report_id"]

            try:
                report = Report.objects.get(report_id=report_id)
            except Report.DoesNotExist:
                return Response(
                    {"error": "Report does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if report.status != "FORWARDED TO POLICE":
                return Response(
                    {"error": "Only forwarded reports can be received by the police."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if report.police_status == "RECEIVED":
                return Response(
                    {
                        "error": f"Report has already been received by officer: {report.assigned_officer}."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            report.police_status = "RECEIVED"
            report.assigned_officer = police_instance
            report.save()

            return Response(
                {
                    "message": "Report received successfully.",
                    "police_status": report.police_status,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseReportView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CloseReportSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        user = request.user
        if user.is_genderdesk:
            genderdesk_instance, _ = GenderDesk.objects.get_or_create(user=user)
        elif user.is_police:
            police_instance, _ = Police.objects.get_or_create(user=user)

        if serializer.is_valid():
            report_id = serializer.validated_data["report_id"]

            try:
                report = Report.objects.get(report_id=report_id)
            except Report.DoesNotExist:
                return Response(
                    {"error": "Report does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not (user.is_genderdesk or user.is_police):
                return Response(
                    {
                        "error": "Only GenderDesk or Police personnel can close the report."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            if report.status == "RESOLVED":
                return Response(
                    {"error": "The report has already been closed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user.is_police:
                if report.status != "FORWARDED TO POLICE":
                    return Response(
                        {
                            "error": "Only reports forwarded to the police can be closed by the police."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif report.police_status != "RECEIVED":
                    return Response(
                        {"error": "Only received reports can be closed."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if user.is_genderdesk and report.assigned_gd != genderdesk_instance:
                return Response(
                    {
                        "error": "Only the assigned GenderDesk member can close the report."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            elif user.is_police and report.assigned_officer != police_instance:
                return Response(
                    {"error": "Only the assigned Police officer can close the report."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            report.status = "RESOLVED"
            report.save()

            if user.is_genderdesk:
                user.profile.report_count += 1
            elif user.is_police:
                user.profile.report_count += 1
            user.profile.save()

            return Response(
                {"message": "Report closed successfully.", "status": report.status},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
