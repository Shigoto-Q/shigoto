import datetime
import typing

from shigoto_q.tasks import enums
from shigoto_q.tasks import models as task_models


class UserTask(
    typing.NamedTuple(
        "UserTask",
        [
            ("id", int),
            ("external_task_id", str),
            ("task_name", str),
            ("schedule", str),
            ("one_off", bool),
            ("enabled", bool),
            ("total_run_count", int),
            ("last_run_at", datetime.datetime),
            ("task_type", int),
        ],
    )
):
    @classmethod
    def from_model(cls, task: task_models.UserTask):
        return cls(
            id=task.id,
            external_task_id=task.external_task_id,
            task_name=task.name,
            schedule=task.schedule,
            one_off=task.one_off,
            enabled=task.enabled,
            total_run_count=task.total_run_count,
            last_run_at=task.last_run_at,
            task_type=task.task_type,
        )


class UserDockerImage(
    typing.NamedTuple(
        "UserTask",
        [
            ("name", str),
            ("repository", str),
            ("image_name", str),
            ("command", str),
        ],
    )
):
    @classmethod
    def from_model(cls, image: task_models.TaskImage):
        return cls(
            name=image.name,
            repository=image.repository,
            image_name=image.image_name,
            command=image.command,
        )
