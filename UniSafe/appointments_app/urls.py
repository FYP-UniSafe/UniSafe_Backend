from django.urls import path
from .views import *

urlpatterns = [
    path("create", CreateAppointmentView.as_view(), name="create-appointment"),
    path('accept/<str:pk>/', AcceptAppointmentView.as_view(), name='accept_appointment'),
    path('list/requested', StudentAppointmentsListView.as_view(), name='student_appointments'),
    path('cancel/<str:pk>/', CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('list/all', ConsultantAppointmentsListView.as_view(), name='consultant_appointments'),
]