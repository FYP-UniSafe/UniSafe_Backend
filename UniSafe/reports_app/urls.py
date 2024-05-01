from django.urls import path
from .views import *

urlpatterns = [
    path("create", CreateReportView.as_view(), name="create-report"),
    path('anonymous/create', CreateAnonymousReportView.as_view(), name='create_anonymous_report'),
    
    path("accept", AcceptReportView.as_view(), name="accept-report"),
    path("anonymous/accept", AcceptAnonymousReportView.as_view(), name="accept-anonymous-report"),

    path("reject", RejectReportView.as_view(), name="reject-report"),
    path("anonymous/reject", RejectAnonymousReportView.as_view(), name="reject-anonymous-report"),

    path("forward", ForwardReportView.as_view(), name="forward-report"),
    path("anonymous/forward", ForwardAnonymousReportView.as_view(), name="forward-anonymous-report"),

    path("receive", ReceiveReportView.as_view(), name="receice-report"),
    path("anonymous/receive", ReceiveAnonymousReportView.as_view(), name="receive-anonymous-report"),

    path("close", CloseReportView.as_view(), name="close-report"),
    path("anonymous/close", CloseAnonymousReportView.as_view(), name="close-anonymous-report"),

    path('list', ListAllReportsView.as_view(), name='list-all-reports'),
    path('anonymous/list', ListAllAnonymousReportsView.as_view(), name='list-all-anonymous-reports'),


    path('list/created', StudentReportsListView.as_view(), name='student-reports-list'),

    path('list/assigned', AssignedReportsListView.as_view(), name='genderdesk-reports-list'),
    path('anonymous/list/assigned', AssignedAnonymousReportsListView.as_view(), name='assigned-anonymous-reports-list'),

    path('list/forwarded', ForwardedReportsListView.as_view(), name='forwarded-reports-list'),
    path('anonymous/list/forwarded', ForwardedAnonymousReportsListView.as_view(), name='forwarded-anonymous-reports-list'),
]

