from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shigoto_q.tasks.models import TaskImage, UserTask

try:
    ALLOW_EDITS = settings.DJANGO_CELERY_RESULTS["ALLOW_EDITS"]
except (AttributeError, KeyError):
    ALLOW_EDITS = False
    pass

from .models import TaskResult


class TaskResultAdmin(admin.ModelAdmin):
    """Admin-interface for results of tasks."""

    model = TaskResult
    date_hierarchy = "date_done"
    list_display = ("task_id", "task_name", "date_done", "status", "worker")
    list_filter = ("status", "date_done", "task_name", "worker")
    readonly_fields = ("date_created", "date_done", "result")
    search_fields = ("task_name", "task_id", "status", "task_args", "task_kwargs")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "task_id",
                    "task_name",
                    "status",
                    "worker",
                    "user",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            _("Parameters"),
            {
                "fields": (
                    "task_args",
                    "task_kwargs",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            _("Result"),
            {
                "fields": (
                    "result",
                    "date_created",
                    "date_done",
                    "traceback",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if ALLOW_EDITS:
            return self.readonly_fields
        else:
            return list(set([field.name for field in self.opts.local_fields]))


admin.site.register(TaskResult, TaskResultAdmin)


@admin.register(TaskImage)
class TaskImageAdmin(admin.ModelAdmin):
    list_display = ("id", "repo_url", "full_name", "image_name")


@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "task",
        "interval",
        "crontab",
        "solar",
        "clocked",
        "args",
        "kwargs",
        "queue",
        "exchange",
        "routing_key",
        "headers",
        "priority",
        "expires",
        "expire_seconds",
        "one_off",
        "start_time",
        "enabled",
        "last_run_at",
        "total_run_count",
        "date_changed",
        "description",
        "task_type",
        "image",
    )
    list_filter = (
        "interval",
        "crontab",
        "solar",
        "clocked",
        "expires",
        "one_off",
        "start_time",
        "enabled",
        "last_run_at",
        "date_changed",
        "image",
    )
    search_fields = ("name",)
