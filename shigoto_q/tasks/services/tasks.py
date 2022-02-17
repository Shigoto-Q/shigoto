from __future__ import absolute_import

import logging
import inspect

from django.db import transaction
from kombu.utils.json import loads

from shigoto_q.tasks import models as task_models
from shigoto_q.tasks import enums as task_enums

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[TASK_SERVICES]"


def run_task(app, task_id: int) -> dict:
    logger.info(f"{_LOG_PREFIX} Running task {task_id}")
    app.loader.import_default_modules()
    tasks = task_models.UserTask.objects.filter(id=task_id)
    celery_task = [(app.tasks.get(task.task), loads(task.kwargs)) for task in tasks]
    if any(task is None for task in tasks):
        for task in tasks:
            if task is None:
                break
        not_found_name = tasks[0].name
        return {"message": f"No valid task for {not_found_name}"}
    task_ids = [task.apply_async(kwargs=kwargs) for task, kwargs in celery_task]
    return {"message": "success"}


def get_all_task_types():
    return list(map(lambda task: task.value._asdict(), task_enums.TaskEnum))


def create_task(kwargs):
    kwargs = parse_params(kwargs)
    logger.info(f"{_LOG_PREFIX} Creating task with kwargs={kwargs}")
    task_result = task_models.TaskResult.objects.create(**kwargs)
    task_result.save()
    return task_result


def update_task_result(kwargs: dict, task_id: int) -> task_models.TaskResult:
    task_result = task_models.TaskResult.objects.get(task_id=task_id)
    with transaction.atomic():
        for k, v in kwargs.items():
            setattr(task_result, k, v)
        task_result.save()
    logger.info(
        f"{_LOG_PREFIX} Updating TaskResult(task_id={task_id}) with kwargs={kwargs}"
    )
    return task_result


def parse_params(kwargs: dict) -> dict:
    accepted_fields = [
        field.name for field in task_models.TaskResult._meta.get_fields()
    ]
    return {k: v for k, v in kwargs.items() if k in accepted_fields}
