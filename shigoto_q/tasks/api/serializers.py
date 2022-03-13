from __future__ import absolute_import

import json

from django.contrib.auth import get_user_model
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from rest_framework import serializers
from rest_framework.fields import Field

from services.internal_docker.client import DockerImageService
from shigoto_q.tasks.models import TaskResult, UserTask

from shigoto_q.tasks.models import TaskImage
from shigoto_q.tasks.enums import TaskEnum

from rest.serializers import CamelCaseSerializer
from rest.fields import JSONField


User = get_user_model()


class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskResultSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = TaskResult
        fields = [
            "task_id",
            "task_name",
            "task_kwargs",
            "status",
            "result",
            "traceback",
            "exception",
            "date_done",
            "date_created",
            "user",
            "user_id",
        ]

    def get_group_name(self):
        return "result"


class TimezoneField(Field):
    """
    Serializing TimeZoneFild
    """

    def to_representation(self, obj):
        return obj.zone

    def to_internal_value(self, data):
        return data


class CrontabSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = [
            "id",
            "minute",
            "hour",
            "day_of_month",
            "month_of_year",
            "day_of_week",
        ]


class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = ["every", "period"]


class ClockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = ["clocked_time"]


class SolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarSchedule
        fields = ["event", "latitude", "longitude"]


class TaskGetSerializer(serializers.ModelSerializer):
    crontab = CrontabSerializer()

    class Meta:
        model = PeriodicTask
        fields = [
            "id",
            "name",
            "task",
            "crontab",
            "interval",
            "clocked",
            "solar",
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
        ]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = [
            "id",
            "name",
            "task",
            "crontab",
            "interval",
            "clocked",
            "solar",
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
        ]


class TaskImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskImage
        fields = ["full_name", "repo_url", "image_name", "command"]

    def validate(self, attrs):
        try:
            DockerImageService.create_image(
                repo_url=attrs.get("repo_url"),
                full_name=attrs.get("full_name"),
                image_name=attrs.get("image_name"),
            )
            return attrs
        except:
            raise serializers.ValidationError(
                "There was an error while pushing your image to Docker."
            )


class TaskPostSerializer(serializers.ModelSerializer):
    def get_task(self, obj):
        return "shigoto_q.tasks.tasks." + obj.get("task")

    class Meta:
        model = UserTask
        fields = [
            "name",
            "task",
            "task_type",
            "image",
            "crontab",
            "interval",
            "clocked",
            "solar",
            "args",
            "kwargs",
            "queue",
            "priority",
            "expires",
            "expire_seconds",
            "one_off",
            "enabled",
        ]

    def create(self, validated_data):
        kwargs = json.loads(validated_data.get("kwargs"))
        kwargs.update({"user": self.context["request"].user})
        kwargs.update({"task_name": validated_data.get("name")})

        image = None

        if validated_data.get("task_type") == TaskEnum.KUBERNETES_JOB.value:
            image_serializer = TaskImageSerializer(data=kwargs)
            if image_serializer.is_valid(raise_exception=True):
                image = image_serializer.save()

        task_created = UserTask.objects.create(
            task=self.get_task(validated_data),
            task_type=validated_data.get("task_type"),
            image=image,
            crontab=validated_data.get("crontab"),
            interval=validated_data.get("interval"),
            clocked=validated_data.get("clocked"),
            solar=validated_data.get("solar"),
            name=validated_data.get("name"),
            kwargs=json.dumps(kwargs),
            args=validated_data.get("args"),
            queue=validated_data.get("queue"),
            priority=validated_data.get("priority"),
            expires=validated_data.get("expires"),
            expire_seconds=validated_data.get("expire_seconds"),
            one_off=validated_data.get("one_off"),
            enabled=validated_data.get("enabled"),
        )

        return task_created


class UserTaskImageSerializer(CamelCaseSerializer):
    full_name = serializers.CharField()
    repo_url = serializers.CharField()
    image_name = serializers.CharField()
    command = serializers.CharField()


class TaskLoadSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=True)
    task_type = serializers.IntegerField(required=True)
    image = UserTaskImageSerializer(required=False, allow_null=True)
    crontab_id = serializers.IntegerField(default=None, required=False, allow_null=True)
    interval_id = serializers.IntegerField(
        default=None, required=False, allow_null=True
    )
    solar_id = serializers.IntegerField(default=None, required=False, allow_null=True)
    clocked_id = serializers.IntegerField(default=None, required=False, allow_null=True)
    args = serializers.ListField(default=[], allow_null=True)
    kwargs = serializers.DictField(default=None, required=False)
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
    task_type = serializers.IntegerField(required=True)
    image = UserTaskImageSerializer(required=False, allow_null=True)
    crontab_id = serializers.IntegerField(required=False, allow_null=True)
    interval_id = serializers.IntegerField(required=False, allow_null=True)
    solar_id = serializers.IntegerField(required=False, allow_null=True)
    clocked_id = serializers.IntegerField(required=False, allow_null=True)
    args = serializers.ListField(default=None, allow_null=True)
    kwargs = serializers.DictField(required=False, default=None, allow_null=True)
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
    task_type = serializers.IntegerField(required=False)
    image = UserTaskImageSerializer(required=False, allow_null=True)
    crontab_id = serializers.IntegerField(required=False, allow_null=True)
    interval_id = serializers.IntegerField(required=False, allow_null=True)
    solar_id = serializers.IntegerField(required=False, allow_null=True)
    clocked_id = serializers.IntegerField(required=False, allow_null=True)
    args = serializers.CharField(required=False)
    kwargs = JSONField(required=False)
    queue = serializers.IntegerField(required=False, allow_null=True)
    priority = serializers.IntegerField(required=False, allow_null=True)
    expires = serializers.IntegerField(required=False, allow_null=True)
    expire_seconds = serializers.IntegerField(required=False, allow_null=True)
    one_off = serializers.BooleanField(default=False, required=False)
    enabled = serializers.BooleanField(default=False, required=False)
