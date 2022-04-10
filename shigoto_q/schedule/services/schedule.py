import logging

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    ClockedSchedule,
    SolarSchedule,
)


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[SCHEDULE-SERVICES]"


def create_interval_schedule(data):
    logger.info(f"{_LOG_PREFIX} Creating new interval schedule(data={data}).")
    return IntervalSchedule.objects.create(**data).__dict__


def create_crontab_schedule(data):
    logger.info(f"{_LOG_PREFIX} Creating new crontab schedule(data={data}).")
    return CrontabSchedule.objects.create(**data).__dict__


def create_clocked_schedule(data):
    logger.info(f"{_LOG_PREFIX} Creating new clocked schedule(data={data}).")
    return ClockedSchedule.objects.create(**data).__dict__


def create_solar_schedule(data):
    logger.info(f"{_LOG_PREFIX} Creating new solar schedule(data={data}).")
    return SolarSchedule.objects.create(**data).__dict__
