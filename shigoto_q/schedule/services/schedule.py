import logging

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    ClockedSchedule,
    SolarSchedule,
)

from shigoto_q.schedule.models import FavoriteSchedule
from shigoto_q.schedule.exceptions import (
    AtleastOneScheduleError,
    MultipleSchedulesSetError,
)


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[SCHEDULE-SERVICES]"


def create_interval_schedule(data: dict) -> dict:
    logger.info(f"{_LOG_PREFIX} Creating new interval schedule(data={data}).")
    return IntervalSchedule.objects.create(**data).__dict__


def create_crontab_schedule(data: dict) -> dict:
    logger.info(f"{_LOG_PREFIX} Creating new crontab schedule(data={data}).")
    return CrontabSchedule.objects.create(**data).__dict__


def create_clocked_schedule(data: dict) -> dict:
    logger.info(f"{_LOG_PREFIX} Creating new clocked schedule(data={data}).")
    return ClockedSchedule.objects.create(**data).__dict__


def create_solar_schedule(data: dict) -> dict:
    logger.info(f"{_LOG_PREFIX} Creating new solar schedule(data={data}).")
    return SolarSchedule.objects.create(**data).__dict__


def create_favorite_schedule(data: dict) -> dict:
    logger.info(f"{_LOG_PREFIX} Creating new favorite schedule(data={data}).")
    _validate_set_schedule(data=data)
    return FavoriteSchedule.objects.create(**data).__dict__


def _validate_set_schedule(data: dict) -> None:
    schedule_types = ["interval", "crontab", "solar", "clocked"]
    selected_schedule_types = [s for s in schedule_types if data.get(s)]

    if len(selected_schedule_types) == 0:
        raise AtleastOneScheduleError(
            "One of clocked, interval, crontab, or solar " "must be set."
        )

    err_msg = "Only one of clocked, interval, crontab, " "or solar must be set"
    if len(selected_schedule_types) > 1:
        error_info = {}
        for selected_schedule_type in selected_schedule_types:
            error_info[selected_schedule_type] = [err_msg]
        raise MultipleSchedulesSetError(error_info)
