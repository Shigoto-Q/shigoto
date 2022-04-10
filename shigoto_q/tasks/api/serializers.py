from __future__ import absolute_import

from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest.serializers import CamelCaseSerializer

User = get_user_model()


class TaskResultSerializer(CamelCaseSerializer):
    task_id = serializers.CharField(required=False)
    task_name = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    user = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=False)
    finished_at = serializers.DateTimeField(required=False)


class DockerImageDeleteSerializer(CamelCaseSerializer):
    id = serializers.IntegerField()


class UserTaskImageSerializer(CamelCaseSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    repository = serializers.CharField(required=False)
    image_name = serializers.CharField(required=False)
    command = serializers.CharField(required=False)


class SimpleHttpOperatorSerializer(CamelCaseSerializer):
    request_endpoint = serializers.URLField(required=True)
    user_id = serializers.IntegerField(required=True)
    task_name = serializers.CharField(
        default="shigoto_q.tasks.tasks.simple_http_operator"
    )


class TaskLoadSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=True)
    type = serializers.IntegerField(required=True)
    image = UserTaskImageSerializer(required=False, allow_null=True)
    crontab_id = serializers.IntegerField(default=None, required=False, allow_null=True)
    interval_id = serializers.IntegerField(
        default=None, required=False, allow_null=True
    )
    solar_id = serializers.IntegerField(default=None, required=False, allow_null=True)
    clocked_id = serializers.IntegerField(default=None, required=False, allow_null=True)
    http_endpoint = serializers.URLField(required=False)
    queue = serializers.IntegerField(default=None, required=False, allow_null=True)
    priority = serializers.IntegerField(default=None, required=False, allow_null=True)
    expires = serializers.IntegerField(default=None, required=False, allow_null=True)
    expire_seconds = serializers.IntegerField(
        default=None, required=False, allow_null=True
    )
    one_off = serializers.BooleanField(required=False)
    enabled = serializers.BooleanField(required=False)


class TaskDumpSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=True)
    type = serializers.IntegerField(required=True)
    image = UserTaskImageSerializer(required=False, allow_null=True)
    crontab_id = serializers.IntegerField(required=False, allow_null=True)
    interval_id = serializers.IntegerField(required=False, allow_null=True)
    solar_id = serializers.IntegerField(required=False, allow_null=True)
    clocked_id = serializers.IntegerField(required=False, allow_null=True)
    queue = serializers.IntegerField(default=None, required=False, allow_null=True)
    priority = serializers.IntegerField(default=None, required=False, allow_null=True)
    expires = serializers.IntegerField(default=None, required=False, allow_null=True)
    expire_seconds = serializers.IntegerField(
        default=None, required=False, allow_null=True
    )
    one_off = serializers.BooleanField(default=None, allow_null=True)
    enabled = serializers.BooleanField(default=True, allow_null=True)
    user_id = serializers.IntegerField()


class TasksListSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    external_task_id = serializers.UUIDField(required=False)
    type = serializers.IntegerField(required=False)
    image = UserTaskImageSerializer(required=False, allow_null=True)
    crontab_id = serializers.IntegerField(required=False, allow_null=True)
    interval_id = serializers.IntegerField(required=False, allow_null=True)
    solar_id = serializers.IntegerField(required=False, allow_null=True)
    clocked_id = serializers.IntegerField(required=False, allow_null=True)
    one_off = serializers.BooleanField(required=False)
    enabled = serializers.BooleanField(required=False)
    total_run_count = serializers.IntegerField(required=False)
    last_run_at = serializers.DateTimeField(required=False, allow_null=True)
    schedule = serializers.CharField(required=False)


class TaskRunSerializer(CamelCaseSerializer):
    external_task_id = serializers.UUIDField(required=True)
