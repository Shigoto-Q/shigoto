import factory

from shigoto_q.tasks import enums as task_enums
from shigoto_q.tasks.models import UserTask
from tests.factory.schedule.schedule_factory import (
    CrontabFactory,
    IntervalFactory,
    SolarFactory,
)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserTask

    id = factory.Faker("pyint", min_value=0, max_value=10000)
    name = factory.Faker("pystr")
    task = task_enums.TaskTypeEnum.REQUEST_ENDPOINT.value
    crontab = factory.SubFactory(CrontabFactory)
    interval = factory.SubFactory(IntervalFactory)
    solar = factory.SubFactory(SolarFactory)
