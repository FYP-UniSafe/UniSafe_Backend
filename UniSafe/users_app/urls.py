from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('user', UserDetailsView.as_view(), name='user-details'),
    path("signup/student", StudentSignupView.as_view(), name="student-signup"),
    path("signup/genderdesk", GenderDeskSignupView.as_view(), name="genderdesk-signup"),
    path("signup/consultant", ConsultantSignupView.as_view(), name="consultant-signup"),
    path("signup/police", PoliceSignupView.as_view(), name="police-signup"),
    path("otp/verify", VerifyOTPView.as_view(), name="verify-otp"),
    path('otp/resend', ResendOTPView.as_view(), name='resend_otp'),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("profile/student", StudentProfileView.as_view(), name="student-profile"),
    path(
        "profile/genderdesk", GenderDeskProfileView.as_view(), name="genderdesk-profile"
    ),
    path("profile/police", PoliceProfileView.as_view(), name="police-profile"),
    path(
        "profile/consultant", ConsultantProfileView.as_view(), name="consultant-profile"
    ),
    path("student/update", StudentProfileView.as_view(), name="student-update"),
    path(
        "student/profile/update",
        StudentProfileUpdateView.as_view(),
        name="student-profile-update",
    ),
    path(
        "genderdesk/update", GenderDeskProfileView.as_view(), name="genderdesk-update"
    ),
    path(
        "genderdesk/profile/update",
        GenderDeskProfileUpdateView.as_view(),
        name="genderdesk-profile-update",
    ),
    path(
        "consultant/update", ConsultantProfileView.as_view(), name="consultant-update"
    ),
    path(
        "consultant/profile/update",
        ConsultantProfileUpdateView.as_view(),
        name="consultant-profile-update",
    ),
    path("police/update", PoliceProfileView.as_view(), name="police-update"),
    path(
        "police/profile/update",
        PoliceProfileUpdateView.as_view(),
        name="police-profile-update",
    ),
    path("password/change", ChangePasswordView.as_view(), name="change-password"),
    path("password/forgot", ForgotPasswordView.as_view(), name="forgot-password"),
    path("password/reset", ResetPasswordView.as_view(), name="reset-password"),
]
