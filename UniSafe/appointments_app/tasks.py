from celery import shared_task
from django.core.management import call_command

@shared_task
def mark_missed_appointments():
    call_command('mark_missed_appointments')
