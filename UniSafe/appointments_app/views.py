from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated


class CreateAppointmentView(generics.CreateAPIView):
    serializer_class = CreateAppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_student:
            return Response(
                {"error": "Only students can create appointments"}, status=403
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=user.profile)

        return Response(serializer.data, status=201)


class AcceptAppointmentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_consultant:
            return Response(
                {"error": "Only consultants can accept appointments"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the appointment_id from URL kwargs
        appointment_id = self.kwargs.get("pk")

        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"error": f"Appointment {appointment_id} doesn't exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if appointment.status == "SCHEDULED":
            return Response(
                {"error": f"Appointment {appointment_id} has already been accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AcceptAppointmentSerializer(
            instance=appointment, data=request.data
        )
        serializer.is_valid(raise_exception=True)

        appointment = serializer.save(
            status="SCHEDULED",
            consultant=user.profile,
            consultant_phone=user.phone_number,
            consultant_office=user.profile.office,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_student:
            return Response(
                {"error": "Only students can view their appointments"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Appointment.objects.filter(client=self.request.user.profile)
