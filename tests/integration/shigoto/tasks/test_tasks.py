from rest_framework import status


from tests.factory.users.users_factory import UserFactory
from tests.factory.tasks.tasks_factory import TaskFactory


class UserTask:
    """
    Steps:
        Login user
        Create a task(either call the endpoint and do it, or use factories,
         in this case just make a factory and assign he task to the user)
        Edit task
        pytest tests/integration/tasks/test_tasks.py
    """
    
    def test_create(self, regular_user):
        print(regular_user)
        login_url = reverse(
            "user-create"
        )  # find the right url name, username is whatever is created, password in
        # 'secret'
        url = reverse("shigoto.tasks.update-task")
        print(url)
        print(login_url)
        assert url