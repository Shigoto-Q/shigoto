from tests.factory.users.users_factory import UserFactory
from tests.factory.tasks.tasks_factory import TaskFactory


def test_task_update():
    user = UserFactory.build()
    user_task = TaskFactory.build()
    print(user)