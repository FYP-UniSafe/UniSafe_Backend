from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('create', create_report, name='create-report'),
]
