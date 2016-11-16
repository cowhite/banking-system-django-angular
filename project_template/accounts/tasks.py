from __future__ import absolute_import
# from celery.decorators import task
from project_template.celery import Celery


app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task()
def create_pdf(account):
  pass