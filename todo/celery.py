from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
app = Celery('todo')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
from todoapp.models import Todolist, Registration
from datetime import datetime
from django.utils.timezone import get_current_timezone

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
    
@app.task(bind=True)
def reverse(self, string):
	return string[::-1]

@periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
def some_task():

    print "sheesh"
