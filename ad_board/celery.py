import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_board.settings')

app = Celery('ad_board')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
