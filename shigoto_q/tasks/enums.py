import enum


class TaskTypeEnum(enum.Enum):
    REQUEST_ENDPOINT = "shigoto_q.tasks.tasks.request_endpoint"
    KUBERNETES_JOB = "shigoto_q.tasks.tasks.k8s_job"
