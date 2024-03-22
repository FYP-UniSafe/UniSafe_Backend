from django.urls import path
from .views import *

urlpatterns = [
    path("create", CreateReportView.as_view(), name="create-report"),
    path("accept", AcceptReportView.as_view(), name="accept-report"),
    path("reject", RejectReportView.as_view(), name="reject-report"),
    path("forward", ForwardReportView.as_view(), name="forward-report"),
    path("receive", ReceiveReportView.as_view(), name="receice-report"),
    path("close", CloseReportView.as_view(), name="close-report"),
    path('list', ListAllReportsView.as_view(), name='list-all-reports'),
    path('list/created', StudentReportsListView.as_view(), name='student-reports-list'),
    path('list/assigned', AssignedReportsListView.as_view(), name='student-reports-list'),
    path('list/forwarded', ForwardedReportsListView.as_view(), name='forwarded-reports-list'),
]

