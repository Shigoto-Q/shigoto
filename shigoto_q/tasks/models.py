from asgiref.sync import async_to_sync
from celery import states
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask

from utils import enums


ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))
User = get_user_model()


class TaskResult(models.Model):
    task_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Task ID"),
        help_text=_("Celery ID for the task that was run"),
    )
    task_name = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Task name"),
        help_text=_("Name of the task that was run"),
    )
    task_args = models.TextField(
        null=True,
        verbose_name=_("Positional arguments"),
        help_text=_("JSON represantation of the positional arguments"),
    )
    task_kwargs = models.TextField(
        null=True,
        verbose_name=_("Named arguments"),
        help_text=_("JSON represantation of the named arguments"),
    )
    status = models.CharField(
        max_length=50,
        default=states.PENDING,
        choices=TASK_STATE_CHOICES,
        verbose_name=_("Task status"),
        help_text=_("Current state of the task being run"),
    )
    worker = models.CharField(
        max_length=100,
        default=None,
        null=True,
        verbose_name=_("Worker"),
        help_text=_("Worker that executes the tasks"),
    )
    result = models.TextField(
        null=True,
        default=None,
        editable=False,
        verbose_name=_("Task result"),
        help_text=_("The data retuned by the task"),
    )
    traceback = models.TextField(
        null=True,
        default=True,
        verbose_name=_("Traceback"),
        help_text=_("Traceback from the task"),
    )
    date_done = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Task completion datetime"),
        help_text=_("DateTime field when the task finished(in UTC)."),
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name=_("Created datetime"),
        help_text=_("Datetime field when the task was created(in UTC)."),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name=_("User"),
        help_text=_("User who ran the task"),
    )
    task_beat_id = models.IntegerField(
        null=True,
        verbose_name=_("Celery beat ID"),
        help_text=_("Celery beat (periodic task) ID"),
    )

    class Meta:
        ordering = ["-date_done"]
        verbose_name = _("Task Result")
        verbose_name_plural = _("Task results")

    def as_dict(self):
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_args": self.task_args,
            "task_kwargs": self.task_kwargs,
            "status": self.status,
            "result": self.result,
            "traceback": self.traceback,
            "date_done": self.date_done,
            "worker": self.worker,
        }

    def __str__(self):
        return f"<Task: {self.task_id} {self.status}>"


class TaskImage(models.Model):
    repo_url = models.CharField(
        max_length=255, verbose_name=_("Url of the GitHub repository")
    )

    full_name = models.CharField(
        max_length=255, verbose_name=_("Name of the GitHub repository")
    )

    image_name = models.CharField(
        unique=True,
        verbose_name=_("Image name"),
        help_text=_("Name of the Docker image inside user namespace"),
        max_length=255,
    )


class UserTask(PeriodicTask):
    task_type = models.PositiveSmallIntegerField(enums.TaskEnum)
    image = models.OneToOneField(
        TaskImage,
        null=True,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
