from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed


class StudentSignupView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StudentSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        refresh = RefreshToken.for_user(student)
        data = UserSerializer(student).data
        data["tokens"] = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(data, status=status.HTTP_201_CREATED)


class StudentProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentProfileSerializer

    def get_object(self):
        return self.request.user


class StudentProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = StudentProfileUpdateSerializer(
            instance=request.user.student_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            user = request.user
            user_serializer = StudentProfileSerializer(user)
            response_data = {
                "message": "Student profile details updated successfully.",
                "user": user_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenderDeskSignupView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GenderDeskSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gender_desk = serializer.save()

        refresh = RefreshToken.for_user(gender_desk)
        data = UserSerializer(gender_desk).data
        data["tokens"] = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(data, status=status.HTTP_201_CREATED)


class GenderDeskProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenderDeskProfileSerializer

    def get_object(self):
        return self.request.user


class GenderDeskProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = GenderDeskProfileUpdateSerializer(
            instance=request.user.genderdesk_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            user = request.user
            user_serializer = GenderDeskProfileSerializer(user)
            response_data = {
                "message": "GenderDesk profile details updated successfully.",
                "user": user_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultantSignupView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConsultantSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consultant = serializer.save()

        refresh = RefreshToken.for_user(consultant)
        data = UserSerializer(consultant).data
        data["tokens"] = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(data, status=status.HTTP_201_CREATED)


class ConsultantProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConsultantProfileSerializer

    def get_object(self):
        return self.request.user


class ConsultantProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = ConsultantProfileUpdateSerializer(
            instance=request.user.consultant_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            user = request.user
            user_serializer = ConsultantProfileSerializer(user)
            response_data = {
                "message": "Consultant profile details updated successfully.",
                "user": user_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PoliceSignupView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PoliceSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        police = serializer.save()

        refresh = RefreshToken.for_user(police)
        data = UserSerializer(police).data
        data["tokens"] = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(data, status=status.HTTP_201_CREATED)


class PoliceProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PoliceProfileSerializer

    def get_object(self):
        return self.request.user


class PoliceProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = PoliceProfileUpdateSerializer(
            instance=request.user.police_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            user = request.user
            user_serializer = PoliceProfileSerializer(user)
            response_data = {
                "message": "Police profile details updated successfully.",
                "user": user_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_obj = OTP.objects.get(user=user)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        except OTP.DoesNotExist:
            return Response(
                {"message": "OTP does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.now() - otp_obj.timestamp > timedelta(minutes=10):
            return Response(
                {"message": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        if otp_obj.otp == otp:
            user.is_active = True
            user.save()
            return Response({"message": "Account activated"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        user.last_login = timezone.now()
        user.save()

        data = UserSerializer(user).data
        data["tokens"] = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:

            RefreshToken(refresh_token).blacklist()
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except TokenError as e:

            raise AuthenticationFailed("Invalid or expired refresh token")


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            user.send_password_reset_email()
        except User.DoesNotExist:
            pass

        return Response(
            {"detail": "Password reset instructions sent to your email."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_obj = OTP.objects.get(user=user)

        if otp_obj.otp != otp:
            return Response(
                {"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Update password
        user.set_password(new_password)
        user.save()

        # Generate new tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Serialize the response data
        response_data = {
            "detail": "Password reset successfully.",
            "access": access_token,
            "refresh": str(refresh),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        user = request.user

        if not user.check_password(old_password):
            return Response(
                {"detail": "Incorrect old password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        # Generate new refresh tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "detail": "Password changed successfully.",
                "access": access_token,
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )
