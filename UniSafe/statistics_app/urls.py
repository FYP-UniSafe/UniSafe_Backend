from django.urls import path
from .views import *

urlpatterns = [
    path('police-locations', AuxiliaryPoliceLocationsAPIView.as_view(), name='auxiliary-police-locations'),
    path('counts', ReportCountsView.as_view(), name='report-counts'),
    path('per/abusetype', ReportsPerCaseTypeView.as_view(), name='reports-per-abuse-type'),
    path('per/location', ReportsPerLocationView.as_view(), name='reports-per-location'),
    path('per/year', ReportsPerYearView.as_view(), name='reports-per-year' )
]

