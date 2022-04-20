from rest.views.resource import ResourceView

from shigoto_q.schedule.api.serializers import (
    ClockedScheduleSerializer,
    CrontabScheduleSerializer,
    IntervalScheduleSerializer,
    SolarScheduleSerializer,
)
from shigoto_q.schedule.services import schedule as schedule_services


class CrontabScheduleCreateView(ResourceView):
    serializer_load_class = CrontabScheduleSerializer
    serializer_dump_class = CrontabScheduleSerializer

    def execute(self, data):
        return schedule_services.create_crontab_schedule(data)


class ClockedScheduleCreateView(ResourceView):
    serializer_load_class = ClockedScheduleSerializer
    serializer_dump_class = ClockedScheduleSerializer

    def execute(self, data):
        return schedule_services.create_clocked_schedule(data)


class IntervalScheduleCreateView(ResourceView):
    serializer_load_class = IntervalScheduleSerializer
    serializer_dump_class = IntervalScheduleSerializer

    def execute(self, data):
        return schedule_services.create_interval_schedule(data)


class SolarScheduleCreateView(ResourceView):
    serializer_load_class = SolarScheduleSerializer
    serializer_dump_class = SolarScheduleSerializer

    def execute(self, data):
        return schedule_services.create_solar_schedule(data)
