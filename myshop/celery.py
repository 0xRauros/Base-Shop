# WHAT IS A CELERY WORKER?
# A celery worker is a process that handles bookkeeping features like
# sending/receiving queue messages, registering tasks, killing hung tasks,
# tracking status, etc. 
# A worker instance can consume from any number of message queues.

# Launc celery: terminal : celery -A myshop worker -l info 

import os
from celery import Celery

# Default django settings for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings') # for the celery command line program.
app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() # Look for a tasks.py in each app added to INSTALLED_APPS in order to load async tasks defined in.
# Import celery in the __init__.py to ensure it is loaded.

