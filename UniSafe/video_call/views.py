from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import jwt
import datetime
import requests

VIDEOSDK_API_KEY = "65bdacaa-d670-4130-b5ed-0c72d73a69df" 
VIDEOSDK_SECRET_KEY = "1c643bc31a5d4bc4c61195951cb5479a5a1f433611e858fdb0b0442c7644023e" 
VIDEOSDK_API_ENDPOINT = "https://api.videosdk.live/v2"

class GenerateToken(APIView):
    def get(self, request):
        expiration_in_seconds = 600
        expiration = datetime.datetime.now() + datetime.timedelta(seconds=expiration_in_seconds)
        payload = {
            'exp': expiration,
            'apikey': VIDEOSDK_API_KEY,
            'permissions': ["allow_join", "allow_mod"],
        }

        roomId = request.GET.get('roomId', '')
        peerId = request.GET.get('peerId', '')

        if roomId or peerId:
            payload['version'] = 2
            payload['roles'] = ["rtc"]

        if roomId:
            payload['roomId'] = roomId

        if peerId:
            payload['participantId'] = peerId    

        token = jwt.encode(payload, VIDEOSDK_SECRET_KEY, algorithm="HS256")

        return Response({'token': token})

class CreateMeeting(APIView):
    def post(self, request):
        data = request.data
        token = data.get('token')
        res = requests.post(f"{VIDEOSDK_API_ENDPOINT}/rooms", headers={"Authorization": token})
        return Response(res.json())

class ValidateMeeting(APIView):
    def post(self, request, meeting_id):
        data = request.data
        token = data.get('token')
        res = requests.get(f"{VIDEOSDK_API_ENDPOINT}/rooms/validate/{meeting_id}", headers={"Authorization": token})
        return Response(res.json())
