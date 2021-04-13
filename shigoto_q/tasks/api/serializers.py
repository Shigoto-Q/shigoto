from django_celery_beat.models import CrontabSchedule
from rest_framework import serializers


class CrontabSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = ["minute", "hour", "day_of_month", "month_of_year", "day_of_week"]
