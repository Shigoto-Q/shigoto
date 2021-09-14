from __future__ import absolute_import

import logging

from kombu.utils.json import loads

from shigoto_q.tasks import models as task_models

logger = logging.getLogger(__name__)


def run_task(app, task_id: int) -> dict:
    print("HEE-$$$$$$$$$$$$$$$$$$$$$$$$")
    print(__name__)
    logger.warning(f"Running task {task_id}")
    print("HEE-$$$$$$$$$$$$$$$$$$$$$$$$")
    app.loader.import_default_modules()
    tasks = task_models.UserTask.objects.filter(id=task_id)
    celery_task = [(app.tasks.get(task.task), loads(task.kwargs)) for task in tasks]
    if any(task is None for task in tasks):
        for task in tasks:
            if task is None:
                break
            print(task.kwargs)
        not_found_name = tasks[0].name
        return {"message": f"No valid task for {not_found_name}"}
    task_ids = [task.apply_async(kwargs=kwargs) for task, kwargs in celery_task]
    return {"message": "success"}
