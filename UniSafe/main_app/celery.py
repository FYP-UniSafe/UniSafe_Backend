from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_app.settings.base')

app = Celery('UniSafe')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
