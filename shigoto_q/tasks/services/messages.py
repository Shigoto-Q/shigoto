import datetime
import typing

from shigoto_q.docker import models as docker_models
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
            ("type", int),
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
            type=task.type,
        )


class UserDockerImage(
    typing.NamedTuple(
        "UserTask",
        [
            ("name", str),
            ("repository", str),
            ("image_name", str),
            ("command", str),
            ("secret_key", str),
            ("id", int),
        ],
    )
):
    @classmethod
    def from_model(cls, image: docker_models.DockerImage):
        return cls(
            name=image.name,
            repository=image.repository,
            image_name=image.image_name,
            command=image.command,
            secret_key=image.secret_key,
            id=image.id,
        )


class TaskResult(
    typing.NamedTuple(
        "TaskResult",
        [
            ("task_id", str),
            ("task_name", str),
            ("status", int),
            ("user", str),
            ("user_id", int),
            ("finished_at", datetime.datetime),
        ],
    )
):
    @classmethod
    def from_model(cls, task_result: task_models.TaskResult):
        return cls(
            task_id=task_result.task_id,
            task_name=task_result.task_name,
            status=task_result.status,
            user=task_result.user.first_name,
            user_id=task_result.user_id,
            finished_at=task_result.date_done,
        )
