# appointments_app/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from appointments_app.models import Appointment
from .serializers import *
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
import requests
import jwt
import datetime
from django.conf import settings

# VIDEOSDK_API_KEY = settings.VIDEOSDK_API_KEY
# VIDEOSDK_SECRET_KEY = settings.VIDEOSDK_SECRET_KEY
VIDEOSDK_API_KEY = "65bdacaa-d670-4130-b5ed-0c72d73a69df"
VIDEOSDK_SECRET_KEY = "1c643bc31a5d4bc4c61195951cb5479a5a1f433611e858fdb0b0442c7644023e"
VIDEOSDK_API_ENDPOINT = "https://api.videosdk.live/v2"


class CreateMeeting(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        token = data.get("token")
        appointment_id = data.get("appointment_id")

        if not appointment_id:
            return Response(
                {"error": "Appointment ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"error": f"Appointment {appointment_id} doesn't exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        res = requests.post(
            f"{VIDEOSDK_API_ENDPOINT}/rooms", headers={"Authorization": token}
        )

        if res.status_code == 200:
            meeting_data = res.json()
            meeting_id = meeting_data.get("roomId")
            # Update the appointment with the meeting ID
            appointment.meeting_id = meeting_id
            appointment.save()

        return Response(res.json())


class GenerateToken(APIView):
    def get(self, request):
        expiration_in_seconds = 30 * 24 * 60 * 60  # 30 days
        expiration = datetime.datetime.now() + datetime.timedelta(
            seconds=expiration_in_seconds
        )
        payload = {
            "exp": expiration,
            "apikey": VIDEOSDK_API_KEY,
            "permissions": ["allow_join", "allow_mod"],
        }

        roomId = request.GET.get("roomId", "")
        peerId = request.GET.get("peerId", "")

        if roomId or peerId:
            payload["version"] = 2
            payload["roles"] = ["rtc"]

        if roomId:
            payload["roomId"] = roomId

        if peerId:
            payload["participantId"] = peerId

        token = jwt.encode(payload, VIDEOSDK_SECRET_KEY, algorithm="HS256")

        return Response({"token": token})


class ValidateMeeting(APIView):
    def post(self, request, meeting_id):
        data = request.data
        token = data.get("token")
        res = requests.get(
            f"{VIDEOSDK_API_ENDPOINT}/rooms/validate/{meeting_id}",
            headers={"Authorization": token},
        )
        return Response(res.json())
