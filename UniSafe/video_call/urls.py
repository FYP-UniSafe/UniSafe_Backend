from django.urls import path
from .views import GenerateToken, CreateMeeting

urlpatterns = [
    path('get-token/', GenerateToken.as_view(), name='generate_token'),
    path('create-meeting/', CreateMeeting.as_view(), name='create_meeting'),
    # path('validate-meeting/<str:meeting_id>/', ValidateMeeting.as_view(), name='validate_meeting'),
]
