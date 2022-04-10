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
    id = factory.Faker("pyint", min_value=0, max_value=1000)
    every = factory.Faker("pyint", min_value=0, max_value=1000)
    period = factory.Faker(
        "random_element", elements=[x[0] for x in IntervalSchedule.PERIOD_CHOICES]
    )

    class Meta:
        model = IntervalSchedule


class SolarFactory(factory.Factory):
    class Meta:
        model = SolarSchedule
