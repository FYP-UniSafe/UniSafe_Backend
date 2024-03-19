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




class CreateReportAPIView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = CreateReportSerializer

    def perform_create(self, serializer):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return Response({"error": "Authentication Required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the authenticated user is a student
        if not self.request.user.is_student:
            return Response({"error": "Only students are allowed to create reports"}, status=status.HTTP_403_FORBIDDEN)

        # Get the authenticated user
        user = self.request.user

        # Get or create Student instance
        student_instance, _ = Student.objects.get_or_create(user=user)

        # Populate Reporter Contact Details fields from the user's profile
        profile = user.profile
        reporter_data = {
            'reporter': student_instance,
            'reporter_full_name': user.full_name,
            'reporter_gender': user.gender,
            'reporter_email': user.email,
            'reporter_phone': user.phone_number,
            'reporter_college': profile.college,
            'reporter_reg_no': profile.reg_no,
        }

        # Merge reporter_data into serializer data
        serializer_data = serializer.validated_data
        serializer_data.update(reporter_data)

        # Save the report
        serializer.save(**serializer_data)

        # Increment report_count field in user's profile
        profile.report_count += 1
        profile.save()

        # Get the success headers
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)