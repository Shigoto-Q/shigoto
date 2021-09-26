from tests.factory.schedule.schedule_factory import CrontabFactory, IntervalFactory, SolarFactory
from shigoto_q.tasks.models import UserTask
import factory

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserTask

    id = factory.Faker("pyint", min_value=0, max_value=10000)
    name = factory.Faker('pystr')
    task = "shigoto_q.tasks.tasks.request_endpoint"
    crontab = factory.SubFactory(CrontabFactory)
    interval = factory.SubFactory(IntervalFactory)
    solar = factory.SubFactory(SolarFactory)
