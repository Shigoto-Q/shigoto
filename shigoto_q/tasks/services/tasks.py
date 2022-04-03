from __future__ import absolute_import

import json
import logging

from django.core.paginator import Paginator
from django.db import transaction
from kombu.utils.json import loads

from shigoto_q.docker import models as docker_models
from shigoto_q.tasks import enums as task_enums
from shigoto_q.tasks import models as task_models
from shigoto_q.tasks.enums import TaskType, TaskTypeEnum
from shigoto_q.tasks.services import messages as task_messages

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[TASK_SERVICES]"


def run_task(app, external_task_id: int, user) -> dict:
    logger.info(f"{_LOG_PREFIX} Running task {external_task_id}")
    app.loader.import_default_modules()
    tasks = task_models.UserTask.objects.filter(
        external_task_id=external_task_id, user=user
    )
    celery_task = []
    celery_task = [(app.tasks.get(task.task), loads(task.kwargs)) for task in tasks]
    if any(task is None for task in tasks):
        for task in tasks:
            if task is None:
                break
        not_found_name = tasks[0].name
        return {"message": f"No valid task for {not_found_name}"}
    task_ids = [task.apply_async(kwargs=kwargs) for task, kwargs in celery_task]
    return tasks.first().__dict__


def get_all_types():
    return list(map(lambda task: task.value._asdict(), task_enums.TaskEnum))


def create_task(kwargs, user):
    with transaction.atomic():
        if kwargs.get("type") == TaskType.SIMPLE_HTTP_OPERATOR.value:
            kwargs["task"] = TaskTypeEnum.SIMPLE_HTTP_OPERATOR.value
            kwargs["kwargs"] = {
                "url": kwargs.pop("http_endpoint"),
                "user_id": user.id,
                "task_name": kwargs.get("name"),
            }
        task = task_models.UserTask.objects.create(**kwargs)
        task.kwargs = json.dumps(task.kwargs).replace("'", '"')
        task.save()
    logger.info(
        f"{_LOG_PREFIX} Creating Task(id={kwargs.get('id')}, user_id={kwargs.get('user_id')}, task={kwargs.get('task')})"
    )
    return task.__dict__


def create_task_result(kwargs):
    kwargs = parse_params(kwargs)
    logger.info(f"{_LOG_PREFIX} Creating result task with kwargs={kwargs}")
    task_result = task_models.TaskResult.objects.create(**kwargs)
    task_result.save()
    return task_messages.TaskResult.from_model(task_result)._asdict()


def update_task_result(kwargs: dict, task_id: int) -> task_models.TaskResult:
    task_result = task_models.TaskResult.objects.get(task_id=task_id)
    with transaction.atomic():
        for k, v in kwargs.items():
            setattr(task_result, k, v)
        task_result.save()
    logger.info(
        f"{_LOG_PREFIX} Updating TaskResult(task_id={task_id}) with kwargs={kwargs}"
    )
    return task_messages.TaskResult.from_model(task_result)._asdict()


def list_user_tasks(user_id, filters):
    filters = filters or {}
    return [
        task_messages.UserTask.from_model(obj)._asdict()
        for obj in task_models.UserTask.objects.filter(user_id=user_id).filter(
            **filters
        )
    ]


def parse_params(kwargs: dict) -> dict:
    accepted_fields = [
        field.name for field in task_models.TaskResult._meta.get_fields()
    ]
    return {k: v for k, v in kwargs.items() if k in accepted_fields}


def get_user_docker_images(filters: dict, user_id: int) -> list:
    filters = filters or {}
    return [
        task_messages.UserDockerImage.from_model(obj)._asdict()
        for obj in docker_models.DockerImage.objects.filter(user_id=user_id).filter(
            **filters
        )
    ]


def create_docker_image(data):
    with transaction.atomic():
        image = docker_models.DockerImage.objects.create(**data)
        logger.info(f"{_LOG_PREFIX} Creating new docker image with data - {data}")
    return image.__dict__


def delete_docker_image(task_id: int, user_id: int):
    with transaction.atomic():
        docker_models.DockerImage.objects.get(id=task_id, user_id=user_id).delete()


def list_task_results(
    filters: dict,
    ordering: list = None,
):
    return task_models.TaskResult.objects.filter(**filters).order_by(*ordering).select_related("user")
