from django.urls import path
from .views import *

urlpatterns = [
    path("create", CreateReportView.as_view(), name="create-report"),
    path("accept", AcceptReportView.as_view(), name="accept-report"),
    path("reject", RejectReportView.as_view(), name="reject-report"),
    path("forward", ForwardReportView.as_view(), name="forward-report"),
    path("receive", ReceiveReportView.as_view(), name="receice-report"),
    path("close", CloseReportView.as_view(), name="close-report"),
]

