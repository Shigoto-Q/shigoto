import enum


from services.events.events import TaskSuccessEvent, DeploymentEvent, TaskFailureEvent


class Event(enum.Enum):
    DEPLOYMENT = "shigoto.kubernetes.deployment"
    SERVICE = "shigoto.kubernetes.service"
    TASK_SUCCESS = "shigoto.task.success"
    TASK_FAILURE = "shigoto.task.failure"


class EventMapping(enum.Enum):
    DEPLOYMENT = DeploymentEvent
    TASK_SUCCESS = TaskSuccessEvent
    TASK_FAILURE = TaskFailureEvent
