from django.contrib import admin

from .models import TaskImage, TaskResult, UserTask


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task_id",
        "task_name",
        "status",
        "date_done",
        "date_created",
        "user",
        "task_beat_id",
    )
    list_filter = ("date_done", "date_created", "user")


@admin.register(TaskImage)
class TaskImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "repository",
        "name",
        "image_name",
        "command",
        "user",
    )


@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_task_id",
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
        "external_task_id",
        "task_type",
        "image",
        "user",
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
        "user",
    )
    search_fields = ("name",)
