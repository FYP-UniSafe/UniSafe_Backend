from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_app.settings.base')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings.prod")

app = Celery('UniSafe')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
