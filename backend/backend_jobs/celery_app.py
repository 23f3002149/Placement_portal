from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Celery app create karo
celery_app = Celery(__name__)

# Redis broker aur backend configure karo
celery_app.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery_app.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
celery_app.conf.task_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_serializer = 'json'
celery_app.conf.timezone = 'UTC'
celery_app.conf.enable_utc = True
