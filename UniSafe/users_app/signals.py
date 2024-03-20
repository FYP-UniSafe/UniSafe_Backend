# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        profile, created = Student.objects.get_or_create(user=instance)
        if not created:
            profile.save()
    elif created and instance.is_genderdesk:
        profile, created = GenderDesk.objects.get_or_create(user=instance)
        if not created:
            profile.save()
    elif created and instance.is_consultant:
        profile, created = Consultant.objects.get_or_create(user=instance)
        if not created:
            profile.save()
    elif created and instance.is_police:
        profile, created = Police.objects.get_or_create(user=instance)
        if not created:
            profile.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
