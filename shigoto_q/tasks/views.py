from __future__ import absolute_import

from time import sleep

from django.contrib.auth import get_user_model

from config.celery_app import app
from rest.common.fetch import fetch_and_paginate
from rest.views import ResourceListView, ResourceView
from shigoto_q.tasks.api.serializers import (
    DockerImageDeleteSerializer,
    TaskDumpSerializer,
    TaskLoadSerializer,
    TaskResultSerializer,
    TaskRunSerializer,
    TasksListSerializer,
    UserImageCreateDumpSerializer,
    UserImageCreateLoadSerializer,
    UserTaskImageSerializer,
)
from shigoto_q.tasks.services import tasks as task_services
from shigoto_q.tasks.services.messages import TaskResult, UserTask, UserDockerImage

User = get_user_model()


class TaskResultListView(ResourceListView):
    serializer_dump_class = TaskResultSerializer
    serializer_load_class = TaskResultSerializer
    owner_check = True

    def fetch(self, filters, pagination):
        return fetch_and_paginate(
            func=task_services.list_task_results,
            filters=filters,
            pagination=pagination,
            serializer_func=TaskResult.from_model,
        )


class DockerImageDeleteView(ResourceView):
    serializer_dump_class = DockerImageDeleteSerializer
    serializer_load_class = DockerImageDeleteSerializer
    owner_check = True

    def execute(self, data):
        return task_services.delete_docker_image(
            task_id=data.get("id"),
            user_id=data.get("user_id"),
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

    def fetch(self, filters, pagination):
        return fetch_and_paginate(
            func=task_services.get_user_docker_images,
            filters=filters,
            pagination=pagination,
            serializer_func=UserDockerImage.from_model
        )


class UserTaskListView(ResourceListView):
    serializer_dump_class = TasksListSerializer
    serializer_load_class = TasksListSerializer

    def fetch(self, filters, pagination):
        return fetch_and_paginate(
            task_services.list_user_tasks,
            filters=filters,
            pagination=pagination,
            serializer_func=UserTask.from_model,
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
