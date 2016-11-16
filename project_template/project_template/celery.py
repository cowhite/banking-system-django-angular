from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_template.settings')
app = Celery('project_template')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
CELERYBEAT_SCHEDULE = {
    # crontab(hour=0, minute=0, day_of_week='saturday')
    'schedule-name': {  # example: 'file-backup'
        'task': 'some_django_app.tasks....',  # example: 'files.tasks.cleanup'
        'schedule': crontab()
    },
}
# if you want to place the schedule file relative to your project or something:
# CELERYBEAT_SCHEDULE_FILENAME = "some/path/and/filename"