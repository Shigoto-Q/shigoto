import enum

from shigoto_q.tasks import messages as task_messages


class TaskTypeEnum(enum.Enum):
    REQUEST_ENDPOINT = "shigoto_q.tasks.tasks.request_endpoint"
    KUBERNETES_JOB = "shigoto_q.tasks.tasks.k8s_job"


class TaskEnum(enum.Enum):
    CUSTOM_ENDPOINT = task_messages.Task(1, "Custom endpoint", "custom_endpoint")
    KUBERNETES_JOB = task_messages.Task(2, "Kubernetes job", "kubernetes_job")


class TaskStatus(enum.Enum):
    PENDING = (0, "PENDING")
    RECEIVED = (1, "RECEIVED")
    STARTED = (2, "STARTED")
    SUCCESS = (3, "SUCCESS")
    FAILURE = (4, "FAILURE")
    REVOKED = (5, "REVOKED")
    REJECTED = (6, "REJECTED")
    RETRY = (7, "RETRY")
    IGNORED = (8, "IGNORED")

    @classmethod
    def get_value(cls, name):
        return cls[name]

    @classmethod
    def get_values(cls):
        return [status.value for status in cls]


class LogEvent(enum.Enum):
    TASK_RESULTS = "task_results"
    TASK_COUNT = "task_count"
