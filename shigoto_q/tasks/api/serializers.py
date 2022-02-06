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
from rest_framework.fields import Field, CharField

from services.job_services import ImageService
from shigoto_q.tasks.models import TaskResult, UserTask

from shigoto_q.tasks.models import TaskImage
from shigoto_q.tasks.enums import TaskEnum

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
            image_service = ImageService()
            image_service.create_image(
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
        kwargs.update({"user": self.context["request"].user.id})
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

        self.context["request"].user.task.add(task_created)
        return task_created
