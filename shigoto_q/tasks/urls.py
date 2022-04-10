from __future__ import absolute_import

from django.urls import path

from shigoto_q.tasks import views

app_name = "tasks"

urlpatterns = [
    path(
        "task/create/",
        views.TaskCreateView.as_view(),
        name="task.create",
    ),
    path(
        "tasks/list/",
        views.UserTaskListView.as_view(),
        name="tasks.list",
    ),
    path(
        "task/run/",
        views.TaskRunView.as_view(),
        name="task.run",
    ),
    path(
        "tasks/results/list/",
        views.TaskResultListView.as_view(),
        name="tasks.result.list",
    ),
    path(
        "docker/images/list/",
        views.UserImageListView.as_view(),
        name="docker.images-list",
    ),
    path(
        "docker/images/delete/",
        views.DockerImageDeleteView.as_view(),
        name="docker.images-delete",
    ),
]
