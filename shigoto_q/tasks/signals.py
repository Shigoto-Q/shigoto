import os

from asgiref.sync import async_to_sync
from celery.signals import (
    celeryd_after_setup,
    task_failure,
    task_prerun,
    task_received,
    task_success,
)
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask

from .models import TaskResult

User = get_user_model()


@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    queue_name = "{0}.dq".format(sender)
    print(queue_name)
    instance.app.amqp.queues.select_add(queue_name)


@task_prerun.connect
def task_prerun_handler(sender=None, *args, **kwargs):
    user = User.objects.get(id=kwargs.get("kwargs").get("user"))
    task_result = TaskResult.objects.create(task_id=kwargs["task_id"])
    task_result.task_kwargs = str(kwargs.get("kwargs", None))
    task_result.task_args = kwargs.get("args", None)
    task_result.task_name = kwargs.get("kwargs").get("task_name")
    task_result.user = user
    task_result.save()


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    task_result = TaskResult.objects.get(task_id=sender.request.id)
    task_result.result = result
    task_result.status = "SUCCESS"
    task_result.save()


@task_failure.connect
def task_failure_handler(sender=None, traceback=None, **kwargs):
    task_result = TaskResult.objects.get(task_id=sender.request.id)
    task_result.traceback = traceback
    task_result.status = "FAILURE"
    task_result.save()
