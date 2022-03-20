import enum

from django.db import models

from shigoto_q.tasks import messages as task_messages


class TaskTypeEnum(enum.Enum):
    SIMPLE_HTTP_OPERATOR = "shigoto_q.tasks.tasks.simple_http_operator"
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


class TaskType(models.IntegerChoices):
    SIMPLE_HTTP_OPERATOR = 0
    KUBERNETES_OPERATOR = 1
    DOCKER_OPERATOR = 2


class TaskEnum(enum.Enum):
    CUSTOM_ENDPOINT = task_messages.Task(1, "Custom endpoint", "custom_endpoint")
    KUBERNETES_JOB = task_messages.Task(2, "Kubernetes job", "kubernetes_job")


class LogEvent(enum.Enum):
    TASK_RESULTS = "task_results"
    TASK_COUNT = "task_count"
