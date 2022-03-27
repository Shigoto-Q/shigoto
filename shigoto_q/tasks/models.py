import secrets
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    PERIOD_CHOICES,
    SINGULAR_PERIODS,
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

from shigoto_q.tasks import enums

User = get_user_model()


def generate_secret():
    return secrets.token_urlsafe()


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
    status = models.PositiveSmallIntegerField(
        default=enums.TaskStatus.PENDING,
        choices=enums.TaskStatus.choices,
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
    exception = models.TextField(
        null=True,
        default=True,
        verbose_name=_("Exception"),
        help_text=_("Exception from the task"),
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
    repository = models.CharField(
        max_length=255, verbose_name=_("Url of the GitHub repository")
    )

    name = models.CharField(
        max_length=255, verbose_name=_("Name of the GitHub repository")
    )

    image_name = models.CharField(
        unique=True,
        verbose_name=_("Image name"),
        help_text=_("Name of the Docker image inside user namespace"),
        max_length=255,
    )

    command = models.CharField(
        max_length=255,
        help_text=_("Command to execute after image startup."),
        verbose_name=_("Command to execute"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name=_("User"),
    )
    secret_key = models.CharField(
        max_length=512,
        default=generate_secret,
        null=True,
        blank=True,
    )


class UserTask(PeriodicTask):
    external_task_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    task_type = models.PositiveSmallIntegerField(
        choices=enums.TaskType.choices, default=enums.TaskType.SIMPLE_HTTP_OPERATOR
    )  # TODO Rename to type
    image = models.OneToOneField(
        TaskImage,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name=_("User"),
    )

    @property
    def schedule(self):
        if self.interval:
            return self._to_interval_representation(
                every=self.interval.every, self_period=self.interval.period
            )
        if self.crontab:
            return self._to_crontab_representation(crontab=self.crontab)
        if self.solar:
            return self.solar.schedule
        if self.clocked:
            return self._to_clocked_representation(clocked_time=self.clocked)

    @classmethod
    def _to_interval_representation(cls, every, self_period):
        readable_period = None
        if every == 1:
            for period, _readable_period in SINGULAR_PERIODS:
                if period == self_period:
                    readable_period = _readable_period.lower()
                    break
            return "every {}".format(readable_period)
        for period, _readable_period in PERIOD_CHOICES:
            if period == self_period:
                readable_period = _readable_period.lower()
                break
        return "every {} {}".format(every, readable_period)

    @classmethod
    def _cronexp(cls, field):
        """Representation of cron expression."""
        return field and str(field).replace(" ", "") or "*"

    @classmethod
    def _to_crontab_representation(cls, crontab):
        return "{0} {1} {2} {3} {4} (m/h/dM/MY/d) {5}".format(
            cls._cronexp(crontab.minute),
            cls._cronexp(crontab.hour),
            cls._cronexp(crontab.day_of_month),
            cls._cronexp(crontab.month_of_year),
            cls._cronexp(crontab.day_of_week),
            str(crontab.timezone),
        )

    @classmethod
    def _to_clocked_representation(cls, clocked_time):
        return "{}".format(clocked_time)
