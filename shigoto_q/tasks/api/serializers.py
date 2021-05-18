import datetime
import json

from channels.layers import get_channel_layer
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

from ..models import TaskResult

User = get_user_model()


class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = [
            "task_id",
            "task_name",
            "status",
            "result",
            "traceback",
            "date_done",
            "date_created",
            "user",
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


class TaskPostSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField(read_only=True)

    def get_task(self, obj):
        return getattr(obj, "task", "shigoto_q.tasks.tasks.custom_endpoint")

    class Meta:
        model = PeriodicTask
        fields = [
            "name",
            "task",
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

        task_created = PeriodicTask.objects.create(
            task="shigoto_q.tasks.tasks.custom_endpoint",
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
