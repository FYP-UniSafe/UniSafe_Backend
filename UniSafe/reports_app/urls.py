from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path("create", CreateReportAPIView.as_view(), name="create-report"),
]
