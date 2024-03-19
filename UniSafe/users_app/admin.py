from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class StudentProfileInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = "Profile"


class GenderDeskProfileInline(admin.StackedInline):
    model = GenderDesk
    can_delete = False
    verbose_name_plural = "Profile"

class ConsultantProfileInline(admin.StackedInline):
    model = Consultant
    can_delete = False
    verbose_name_plural = "Profile"

class PoliceProfileInline(admin.StackedInline):
    model = Police
    can_delete = False
    verbose_name_plural = "Profile"

class UserAdmin(UserAdmin):
    model = User
    verbose_name_plural = "User"
    inlines = [StudentProfileInline, GenderDeskProfileInline, ConsultantProfileInline, PoliceProfileInline]

    list_display = (
        "id",
        "email",
        "full_name",
        "phone_number",
        "gender",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",)

    search_fields = ['full_name', 'email', 'id']
    ordering = ('date_joined',)


admin.site.register(User, UserAdmin)