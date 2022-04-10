import pytest

from django.urls import reverse

from shigoto_q.tasks.models import UserTask


@pytest.mark.django_db
class TestTaskView:
    url = reverse("shigoto:tasks:task.create")

    def test_without_data(self, regular_client):
        resp = regular_client.post(self.url, {}, format="json")
        assert resp.status_code == 400

    def test_as_normal(self, regular_user, regular_client, interval_schedule):
        data = {
            "name": "Test task3",
            "type": 0,
            "intervalId": interval_schedule.id,
            "httpEndpoint": "https://jsonplaceholder.typicode.com/posts/1",
            "oneOff": False,
        }
        response = regular_client.post(self.url, data=data, format="json")
        assert response.status_code == 200
        assert UserTask.objects.first()
