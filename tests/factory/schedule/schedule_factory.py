import factory
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
)


class CrontabFactory(factory.Factory):
    class Meta:
        model = CrontabSchedule


class ClockedFactory(factory.Factory):
    class Meta:
        model = ClockedSchedule


class IntervalFactory(factory.Factory):
    class Meta:
        model = IntervalSchedule


class SolarFactory(factory.Factory):
    class Meta:
        model = SolarSchedule
