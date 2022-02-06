import enum

from django.db import models
from shigoto_q.tasks import messages as task_messages


class TaskTypeEnum(enum.Enum):
    REQUEST_ENDPOINT = "shigoto_q.tasks.tasks.simple_http_operator"
    KUBERNETES_JOB = "shigoto_q.tasks.tasks.kubernetes"
    DOCKER_JOB = "shigoto_q.tasks.tasks.docker"


class TaskEnum(enum.Enum):
    CUSTOM_ENDPOINT = task_messages.Task(
        1, "Simple HTTP Operator", "simple_http_operator"
    )
    KUBERNETES_JOB = task_messages.Task(2, "Kubernetes cron", "kubernetes")
    DOCKER_JOB = task_messages.Task(3, "Docker cron", "docker")


class TaskStatus(models.IntegerChoices):
    PENDING = 0
    RECEIVED = 1
    STARTED = 2
    SUCCESS = 3
    FAILURE = 4
    REVOKED = 5
    REJECTED = 6
    RETRY = 7
    IGNORED = 8

    @classmethod
    def get_value(cls, name):
        return cls[name]

    @classmethod
    def get_values(cls):
        return [status.value for status in cls]

    @classmethod
    def from_name(cls):
        return


class LogEvent(enum.Enum):
    TASK_RESULTS = "task_results"
    TASK_COUNT = "task_count"
