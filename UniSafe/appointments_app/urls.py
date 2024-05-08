from django.urls import path
from .views import *

urlpatterns = [
    path("create", CreateAppointmentView.as_view(), name="create-appointment"),
    path('accept/<str:pk>/', AcceptAppointmentView.as_view(), name='accept_appointment'),
    path('list/requested', StudentAppointmentsListView.as_view(), name='student_appointments'),
    path('cancel/<int:pk>/', CancelAppointmentView.as_view(), name='cancel_appointment'),
]