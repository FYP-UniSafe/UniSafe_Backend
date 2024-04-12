from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import random
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_student(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_student = True
        user.save(using=self._db)
        user.save()
        return user

    def create_genderdesk(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_genderdesk = True
        user.is_staff = True
        user.save(using=self._db)
        user.save()
        return user

    def create_police(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_police = True
        user.save(using=self._db)
        user.save()
        return user

    def create_consultant(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_consultant = True
        user.save(using=self._db)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=25, blank=False, unique=False)
    phone_number = models.CharField(max_length=15, blank=False)
    gender = models.CharField(max_length=6, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_genderdesk = models.BooleanField(default=False)
    is_police = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def profile(self):
        if self.is_student:
            return self.student_profile
        elif self.is_genderdesk:
            return self.genderdesk_profile
        elif self.is_consultant:
            return self.consultant_profile
        elif self.is_police:
            return self.police_profile
        else:
            return None

    def send_password_reset_email(self):
        if not hasattr(self, "otp"):
            otp = OTP.objects.create(student=self)
        else:
            otp = self.otp

        subject = "Password Reset OTP"
        message_reset = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 30px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    background-color: #efe4ff;
                    align-items: flex-start;
                    padding-left: 5vw;
                }}
                body b {{
                    color: #362555;
                }}
                .otp {{
                    color: #362555;
                }}
            </style>
        </head>
        <body>
            <p>Hi {instance.full_name},<br>You requested to reset your <b>UniSafe</b> password. <br>To reset your password, use the OTP below:</p>
                <h1 class="otp">{otp.otp}</h1>
                <p>This OTP expires in 10 minutes.</p>
                <p style="color: #362555;">Regards,<br>UniSafe Team</p>
                <p style="font-size: 15px;"><small>If you did not request this, please ignore this email.</small></p>
        </body>
        </html>
        """.format(
            instance=self, otp=otp
        )

        # Obtain the plain text version of the email by stripping HTML tags
        plain_message = strip_tags(message_reset)

        # Send email
        send_mail(
            subject,
            plain_message,
            "unisafe.reports@gmail.com",
            [self.email],
            html_message=message_reset,
        )


# OTP Model
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.otp = random.randint(100000, 999999)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_otp_and_send_email(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        otp = OTP.objects.create(user=instance)

        subject = "Your UniSafe OTP"

        html_message = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 30px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    background-color: #efe4ff;
                    align-items: flex-start;
                    padding-left: 5vw;
                }}
                body b {{
                    color: #362555;
                }}
                .otp {{
                    color: #362555;
                }}
            </style>
        </head>
        <body>
            <p>Hi {instance.full_name},<br>Thank you for joining <b>UniSafe.</b><br>To activate your account, use the OTP below:</p>
                <h1 class="otp">{otp.otp}</h1>
                <p>This OTP expires in 10 minutes.</p>
                <p style="color: #362555;">Regards,<br>UniSafe Team</p>
                <p style="font-size: 15px;"><small>If you did not request this, please ignore this email.</small></p>
        </body>
        </html>
        """.format(
            instance=instance, otp=otp
        )

        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject, plain_message, "unisafe.reports@gmail.com", [instance.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()


def resend_otp(email):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return {"error": "Email does not exist. Please sign up."}

    # Check if OTP already exists
    try:
        otp = OTP.objects.get(user=user)
        otp.otp = random.randint(100000, 999999)
        otp.save()
    except OTP.DoesNotExist:
        otp = OTP.objects.create(user=user)

    # Send OTP via email
    subject = "Your UniSafe OTP resend Request"
    html_message = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 30px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                background-color: #efe4ff;
                align-items: flex-start;
                padding-left: 5vw;
            }}
            body b {{
                color: #362555;
            }}
            .otp {{
                color: #362555;
            }}
        </style>
    </head>
    <body>
        <p>Hi {instance.full_name},<br>Thank you for joining <b>UniSafe.</b><br>Your OTP resend request was received, use the OTP below:</p>
            <h1 class="otp">{otp.otp}</h1>
            <p>This OTP expires in 10 minutes.</p>
            <p style="color: #362555;">Regards,<br>UniSafe Team</p>
            <p style="font-size: 15px;"><small>If you did not request this, please ignore this email.</small></p>
    </body>
    </html>
    """.format(
        instance=user, otp=otp
    )

    send_mail(
        subject,
        strip_tags(html_message),
        "unisafe.reports@gmail.com",
        [user.email],
        html_message=html_message,
    )

    return {"message": "OTP resent successfully."}


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="student_profile"
    )
    custom_id = models.CharField(max_length=25, unique=True)
    reg_no = models.CharField(max_length=25, unique=True, blank=False)
    college = models.CharField(max_length=20, blank=False)
    report_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email


class GenderDesk(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="genderdesk_profile",
    )
    custom_id = models.CharField(max_length=25, unique=True)
    staff_no = models.CharField(max_length=25, unique=True, blank=False)
    office = models.CharField(max_length=20)
    report_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email


class Consultant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="consultant_profile",
    )
    custom_id = models.CharField(max_length=25, unique=True)
    staff_no = models.CharField(max_length=25, unique=True, blank=False)
    office = models.CharField(max_length=20)
    session_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email


class Police(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="police_profile"
    )
    custom_id = models.CharField(max_length=25, unique=True)
    police_no = models.CharField(max_length=25, unique=True, blank=False)
    station = models.CharField(max_length=20, blank=False)
    report_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email


@receiver(pre_save)
def set_custom_id(sender, instance, *args, **kwargs):
    if isinstance(instance, Student):
        user_type_prefix = "S"
        student_count = Student.objects.count()
    elif isinstance(instance, GenderDesk):
        user_type_prefix = "G"
        genderdesk_count = GenderDesk.objects.count()
    elif isinstance(instance, Police):
        user_type_prefix = "P"
        police_count = Police.objects.count()
    elif isinstance(instance, Consultant):
        user_type_prefix = "C"
        consultant_count = Consultant.objects.count()
    else:
        return

    if user_type_prefix == "S":
        instance.custom_id = f"{user_type_prefix}{instance.reg_no}-{student_count+1}"
    elif user_type_prefix == "G":
        instance.custom_id = (
            f"{user_type_prefix}{instance.staff_no}-{genderdesk_count+1}"
        )
    elif user_type_prefix == "P":
        instance.custom_id = f"{user_type_prefix}{instance.police_no}-{police_count+1}"
    elif user_type_prefix == "C":
        instance.custom_id = (
            f"{user_type_prefix}{instance.staff_no}-{consultant_count+1}"
        )
