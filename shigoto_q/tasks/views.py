from __future__ import absolute_import

from time import sleep

from django.contrib.auth import get_user_model
from django.http import StreamingHttpResponse

from config.celery_app import app
from rest.views import ResourceListView, ResourceView
from shigoto_q.tasks.api.serializers import (
    TaskDumpSerializer,
    TaskLoadSerializer,
    TaskRunSerializer,
    TasksListSerializer,
    UserImageCreateLoadSerializer,
    UserImageCreateDumpSerializer,
    UserTaskImageSerializer,
    DockerImageDeleteSerializer,
    TaskResultSerializer,
)
from shigoto_q.tasks.models import TaskResult, UserTask
from shigoto_q.tasks.services import tasks as task_services
from utils import enums as task_enums

User = get_user_model()


class TaskResultListView(ResourceListView):
    serializer_dump_class = TaskResultSerializer
    serializer_load_class = TaskResultSerializer
    owner_check = True

    def fetch(self, filters):
        return task_services.list_task_results(filters=filters)



class DockerImageDeleteView(ResourceView):
    serializer_dump_class = DockerImageDeleteSerializer
    serializer_load_class = DockerImageDeleteSerializer
    owner_check = True

    def execute(self, data):
        return task_services.delete_docker_image(
            task_id=data.get('id'),
            user_id=data.get('user_id'),
        )


class DockerImageCreateView(ResourceView):
    http_method_names = ["post"]
    serializer_dump_class = UserImageCreateDumpSerializer
    serializer_load_class = UserImageCreateLoadSerializer
    owner_check = True

    def execute(self, data):
        return task_services.create_docker_image(data=data)


class UserImageListView(ResourceListView):
    serializer_dump_class = UserTaskImageSerializer
    serializer_load_class = UserTaskImageSerializer

    def fetch(self, filters):
        return task_services.get_user_docker_images(
            filters=filters,
            user_id=self.request.user.id,
        )


class UserTaskListView(ResourceListView):
    serializer_dump_class = TasksListSerializer
    serializer_load_class = TasksListSerializer

    def fetch(self, filters):
        return task_services.list_user_tasks(
            user_id=self.request.user.id,
            filters=filters,
        )


class TaskCreateView(ResourceView):
    http_method_names = ["post"]
    serializer_dump_class = TaskDumpSerializer
    serializer_load_class = TaskLoadSerializer
    owner_check = True

    def execute(self, data):
        return task_services.create_task(data, self.request.user)


class TaskRunView(ResourceView):
    http_method_names = ["post"]
    serializer_dump_class = TaskRunSerializer
    serializer_load_class = TaskRunSerializer
    owner_check = True

    def execute(self, data):
        return task_services.run_task(
            app=app,
            external_task_id=data.get("external_task_id"),
            user=self.request.user,
        )
