from django_celery_beat.models import (
    CrontabSchedule,
    IntervalSchedule,
    ClockedSchedule,
    SolarSchedule,
)
from rest_framework import serializers
from rest_framework.fields import Field


class TimezoneField(Field):
    """
    Serializing TimeZoneFild
    """

    def to_representation(self, obj):
        return obj.zone

    def to_internal_value(self, data):
        return data


class CrontabSerializer(serializers.ModelSerializer):
    timezone = TimezoneField()

    class Meta:
        model = CrontabSchedule
        fields = ["minute", "hour", "day_of_month", "month_of_year", "day_of_week"]


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
