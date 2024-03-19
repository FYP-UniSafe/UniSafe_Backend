from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class OTPInline(admin.StackedInline):
    model = OTP
    can_delete = False
    verbose_name_plural = "OTP"
class StudentProfileInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = "Student Profile"

class GenderDeskProfileInline(admin.StackedInline):
    model = GenderDesk
    can_delete = False
    verbose_name_plural = "GenderDesk Profile"

class ConsultantProfileInline(admin.StackedInline):
    model = Consultant
    can_delete = False
    verbose_name_plural = "Consultant Profile"

class PoliceProfileInline(admin.StackedInline):
    model = Police
    can_delete = False
    verbose_name_plural = "Police Profile"

class CustomUserAdmin(BaseUserAdmin):
    model = User
    verbose_name_plural = "Users"

    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    )

    search_fields = ['email', 'id']
    ordering = ('id',)

    def get_inline_instances(self, request, obj=None):
        if obj is not None:
            inlines = []
            if obj.is_student:
                inlines.append(StudentProfileInline)
            elif obj.is_genderdesk:
                inlines.append(GenderDeskProfileInline)
            elif obj.is_consultant:
                inlines.append(ConsultantProfileInline)
            elif obj.is_police:
                inlines.append(PoliceProfileInline)
            inlines.append(OTPInline)
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)
