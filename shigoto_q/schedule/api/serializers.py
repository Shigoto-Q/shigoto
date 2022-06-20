from rest_framework import serializers

from rest.fields import TimezoneField
from rest.serializers import CamelCaseSerializer
from django_celery_beat import models


class CrontabScheduleSerializer(CamelCaseSerializer):
    minute = serializers.CharField(required=False)
    hour = serializers.CharField(required=False)
    day_of_week = serializers.CharField(required=False)
    day_of_month = serializers.CharField(required=False)
    month_of_year = serializers.CharField(required=False)
    timezone = TimezoneField(required=False)


class IntervalScheduleSerializer(CamelCaseSerializer):
    every = serializers.IntegerField(required=False)
    period = serializers.CharField(required=False)


class ClockedScheduleSerializer(CamelCaseSerializer):
    clocked_time = serializers.DateTimeField(required=False)


class SolarScheduleSerializer(CamelCaseSerializer):
    event = serializers.CharField(required=False)
    latitude = serializers.CharField(required=False)
    longitude = serializers.CharField(required=False)



class FavoriteScheduleLoadSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    interval_id = serializers.IntegerField(required=False)
    crontab_id = serializers.IntegerField(required=False)
    clocked_id = serializers.IntegerField(required=False)
    solar_id = serializers.IntegerField(required=False)
