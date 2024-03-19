from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, TokenBackendError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model





#USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'gender', 'is_active', 'is_staff',
                'is_student', 'is_genderdesk', 'is_police', 'is_consultant','date_joined', 'last_login' ]
        
    def to_representation(self, instance):
            data = super().to_representation(instance)
    
            if instance.is_student:
                data.pop('is_genderdesk', None)
                data.pop('is_police', None)
                data.pop('is_consultant', None)
            elif instance.is_genderdesk:
                data.pop('is_student', None)
                data.pop('is_police', None)
                data.pop('is_consultant', None)
            elif instance.is_police:
                data.pop('is_student', None)
                data.pop( 'is_genderdesk', None)
                data.pop('is_consultant', None)
            elif instance.is_consultant:
                data.pop('is_student', None)
                data.pop('is_police', None)
                data.pop('is_genderdesk', None)
            else:
                pass
    
            return data





#STUDENT SERIALIZERS
class StudentProfile(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['reg_no', 'custom_id', 'college', 'report_count']
    
class StudentProfileSerializer(serializers.ModelSerializer):
    profile = StudentProfile()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'gender', 'is_active', 'is_staff',
                'is_student', 'date_joined', 'last_login', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        student = User.objects.create(**validated_data)
        Student.objects.create(user=student, **profile_data)
        return student
    
    def update(self, instance, validated_data):
        # profile_data = validated_data.pop('profile', {})
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
class StudentProfileUpdateSerializer(serializers.Serializer):
    college = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.college = validated_data.get('college', instance.college)
        instance.save()
        return instance
    
class StudentSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    reg_no = serializers.CharField(write_only=True)
    college = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ( 'id', 'email', 'full_name',  'phone_number',  'gender', 'password', 'reg_no', 'college')
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        reg_no = validated_data.pop('reg_no', None)
        college = validated_data.pop('college', None)
        profile_data = {'reg_no': reg_no, 'college': college, 'report_count': 0}
        instance = User.objects.create_student(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        Student.objects.create(user=instance, **profile_data)
        return instance





#GENDERDESK SERIALIZERS
class GenderDeskProfile(serializers.ModelSerializer):
    class Meta:
        model = GenderDesk
        fields = ['staff_no', 'custom_id', 'office', 'report_count']
    
class GenderDeskProfileSerializer(serializers.ModelSerializer):
    profile = GenderDeskProfile()
    
    class Meta:
            model = User
            fields = ['id', 'email', 'full_name', 'phone_number', 'gender', 'is_active', 'is_staff',
                    'is_genderdesk', 'date_joined', 'last_login', 'profile']
    
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        gender_desk = User.objects.create(**validated_data)
        User.objects.create(user=gender_desk, **profile_data)
        return gender_desk
    
    def update(self, instance, validated_data):
        # profile_data = validated_data.pop('profile', {})
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
class GenderDeskProfileUpdateSerializer(serializers.Serializer):
    office = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.office = validated_data.get('office', instance.office)
        instance.save()
        return instance
    
class GenderDeskSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    staff_no = serializers.CharField(write_only=True)
    office = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ( 'email', 'full_name',  'phone_number',  'gender', 'password', 'office', 'staff_no')
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        staff_no = validated_data.pop('staff_no', None)
        office = validated_data.pop('office', None)
        profile_data = {'staff_no': staff_no, 'office': office, 'report_count': 0}
        instance = User.objects.create_genderdesk(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        GenderDesk.objects.create(user=instance, **profile_data)
        return instance





#CONSULTANT SERIALIZERS
class ConsultantProfile(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['staff_no', 'custom_id', 'office', 'session_count']
    
class ConsultantProfileSerializer(serializers.ModelSerializer):
    profile = ConsultantProfile()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'gender', 'is_active', 'is_staff',
                'is_consultant', 'date_joined', 'last_login', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        consultant = User.objects.create(**validated_data)
        User.objects.create(user=consultant, **profile_data)
        return consultant
    
    def update(self, instance, validated_data):
        # profile_data = validated_data.pop('profile', {})
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
class ConsultantProfileUpdateSerializer(serializers.Serializer):
    office = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.office = validated_data.get('office', instance.office)
        instance.save()
        return instance
    
class ConsultantSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    staff_no = serializers.CharField(write_only=True)
    office = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( 'email', 'full_name',  'phone_number',  'gender', 'password', 'office', 'staff_no')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        staff_no = validated_data.pop('staff_no', None)
        office = validated_data.pop('office', None)
        profile_data = {'staff_no': staff_no, 'office': office, 'session_count': 0}
        instance = User.objects.create_consultant(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        Consultant.objects.create(user=instance, **profile_data)
        return instance






#POLICE SERIALIZERS
class PoliceProfile(serializers.ModelSerializer):
    class Meta:
        model = Police
        fields = ['police_no', 'custom_id', 'station', 'report_count']
    
class PoliceProfileSerializer(serializers.ModelSerializer):
    profile = PoliceProfile()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'gender', 'is_active', 'is_staff',
                'is_police', 'date_joined', 'last_login', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        police = User.objects.create(**validated_data)
        User.objects.create(user=police, **profile_data)
        return police
    
    def update(self, instance, validated_data):
        # profile_data = validated_data.pop('profile', {})
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
class PoliceProfileUpdateSerializer(serializers.Serializer):
    station = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.office = validated_data.get('station', instance.station)
        instance.save()
        return instance
    
class PoliceSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    police_no = serializers.CharField(write_only=True)
    station = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ( 'email', 'full_name',  'phone_number',  'gender', 'password', 'station', 'police_no')
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        police_no = validated_data.pop('police_no', None)
        station = validated_data.pop('station', None)
        profile_data = {'police_no': police_no, 'station': station, 'report_count': 0}
        instance = User.objects.create_police(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        Police.objects.create(user=instance, **profile_data)
        return instance





#VERIFY OTP SERIALIZER
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()   





#LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Account is not active.")
                return user
            else:
                raise serializers.ValidationError("Incorrect email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")





#LOGOUT SERIALIZER
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')

        if not refresh_token:
            raise serializers.ValidationError('Refresh token is required.')

        return attrs





#FORGOT PASSWORD SERIALIZER
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email.')
        return value





#RESET PASSWORD SERIALIZER
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email.')
        return value





#CHANGE PASSWORD SERIALIZER
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)