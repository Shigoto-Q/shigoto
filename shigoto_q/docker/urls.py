from django.urls import path

from shigoto_q.docker import views

app_name = "docker"

urlpatterns = [
    path(
        "docker/images/fetch/",
        views.DockerImageListView.as_view(),
        name="shigoto_q.docker.image.list",
    ),
]
