from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status, generics
from django.contrib.auth.models import User
from .serializers import *
from django.db.models import F
# from . import models
from users_app.models import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report(request):
    # Get the authenticated user
    student = request.user
    profile = student
    
    # Check if the authenticated user is a student
    if not student.is_student:
        return JsonResponse({'error': 'Only students can create reports'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.dict()
    
    # Fill reporter details directly in request data
    data.update({
        'reporter': student.id,
        'reporter_full_name': student.full_name,
        'reporter_email': student.email,
        'reporter_phone': student.phone_number,
        'reporter_gender': student.gender,
        'reporter_college': profile.profile.college,
        'reporter_reg_no': profile.profile.reg_no,
    })
    
    serializer = CreateReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)