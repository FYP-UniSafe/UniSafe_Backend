from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from appointments_app.models import Appointment

class Command(BaseCommand):
    help = 'Mark appointments as MISSED if they are more than 2 hours past their start time.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        missed_threshold = now - timedelta(hours=2)

        missed_appointments = Appointment.objects.filter(
            date__lte=missed_threshold.date(),
            start_time__lte=missed_threshold.time(),
            status='SCHEDULED'
        )

        for appointment in missed_appointments:
            appointment.status = 'MISSED'
            appointment.save()
            self.stdout.write(f'Appointment {appointment.appointment_id} marked as MISSED.')
