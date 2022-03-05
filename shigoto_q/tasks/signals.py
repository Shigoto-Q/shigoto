import json
import logging

from celery.signals import (
    before_task_publish,
    task_failure,
    task_prerun,
    task_retry,
    task_success,
    task_revoked,
)
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.db.models import Count, Q
from django.dispatch import receiver

from services.redis.client import RedisClient
from shigoto_q.tasks.models import TaskResult
from shigoto_q.tasks.enums import LogEvent, TaskStatus
from shigoto_q.tasks.services import tasks as task_services
from shigoto_q.tasks.api.serializers import TaskResultSerializer


User = get_user_model()
client = RedisClient
logger = logging.getLogger(__name__)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


@before_task_publish.connect
def task_sent_handler(sender=None, headers=None, body=None, properties=None, **kwargs):
    info = (headers if headers and "task" in headers else body) or {}
    kwargsrepr = info.get("kwargsrepr")
    kwargsrepr = json.loads(kwargsrepr.replace("'", '"'))
    kwargsrepr["task_id"] = info.get("id")
    kwargsrepr["user"] = get_user(kwargsrepr["user"])
    kwargsrepr["status"] = TaskStatus.RECEIVED
    task_result = task_services.create_task_result(kwargsrepr)
    serialized_task_result = TaskResultSerializer(task_result)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))


@task_prerun.connect
def task_prerun_handler(sender=None, *args, **kwargs):
    kwargs = dict(status=TaskStatus.STARTED)
    task_result = task_services.update_task_result(kwargs, sender.request.id)
    serialized_task_result = TaskResultSerializer(task_result)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    kwargs = dict(result=result, status=TaskStatus.SUCCESS)
    task_result = task_services.update_task_result(kwargs, sender.request.id)
    serialized_task_result = TaskResultSerializer(task_result)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))


@task_failure.connect
def task_failure_handler(sender=None, traceback=None, exception=None, **kwargs):
    kwargs = dict(
        traceback=traceback,
        exception=exception,
        status=TaskStatus.FAILURE,
    )
    task_result = task_services.update_task_result(kwargs, sender.request.id)
    serialized_task_result = TaskResultSerializer(task_result)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))


@task_revoked.connect
def task_prerun_handler(sender=None, *args, **kwargs):
    kwargs = dict(status=TaskStatus.REVOKED)
    task_result = task_services.update_task_result(kwargs, sender.request.id)
    serialized_task_result = TaskResultSerializer(task_result)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))


@task_revoked.connect
def task_prerun_handler(sender=None, *args, **kwargs):
    kwargs = dict(status=TaskStatus.RETRY)
    task_result = task_services.update_task_result(kwargs, sender.request.id)
    serialized_task_result = TaskResultSerializer(task_result)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))


@receiver(post_save, sender=TaskResult)
def send_task_count(sender, instance, **kwargs):
    user_id = instance.user_id
    qs = TaskResult.objects.filter(user_id=user_id).aggregate(
        success=Count("pk", filter=Q(status=TaskStatus.SUCCESS)),
        failure=Count("pk", filter=Q(status=TaskStatus.FAILURE)),
        pending=Count("pk", filter=Q(status=TaskStatus.PENDING)),
    )
    qs["userId"] = user_id
    client.publish(LogEvent.TASK_COUNT.value, json.dumps(qs))


@receiver(pre_save, sender=TaskResult)
def send_pre_save_task_status(sender, instance, **kwargs):
    serialized_task_result = TaskResultSerializer(instance)
    client.publish(LogEvent.TASK_RESULTS.value, json.dumps(serialized_task_result.data))
