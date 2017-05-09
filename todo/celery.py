from __future__ import absolute_import
import os
import datetime
from celery import Celery
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import send_mail


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
app = Celery('todo')

# Using a string here means the worker will not have to
# pickle the object when using Windows.

#from django.utils.timezone import get_current_timezone

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
    
@app.task(bind=True)
def reverse(self, string):
    return string[::-1]

@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    from todoapp.models import Todolist, Registration
    from todo import settings
    obj_list= Todolist.objects.all()
    for x in obj_list:
        if x.due_date == None:
            pass
        else:
            date_obj = x.due_date
            print date_obj
            #date_obj = str(date_obj).split('+')[0]
            #obj_date=datetime.datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')    
            mm= (date_obj - datetime.datetime.now())
            print mm
            print mm.total_seconds()/60
            noti_date = mm.total_seconds()/60
            #print x.person_id
            print x.task
            obj = Registration.objects.get(id = x.person_id)
            ss = str(obj.email_id)
            if noti_date > 0 and noti_date <20:
                send_mail('Hii %s' % str(obj.user_name), "Just a reminder that your {%s} task is due soon." %x.task, 'snehatezu@gmail.com', [ss], fail_silently=False)
                #print obj.email_id
