from django.urls import include, path

app_name = "shigoto"

urlpatterns = [
    path(
        "v1/",
        include("shigoto_q.tasks.urls"),
        name="shigoto_q.tasks.urls",
    ),
    path(
        "v1/",
        include("shigoto_q.users.urls"),
        name="shigoto_q.users.urls",
    ),
    path(
        "v1/",
        include("shigoto_q.github.urls"),
        name="shigoto_q.github.urls",
    ),
    path(
        "v1/",
        include("shigoto_q.docker.urls"),
        name="shigoto_q.docker.urls",
    ),
    path(
        "v1/",
        include("shigoto_q.schedule.urls"),
        name="shigoto_q.schedule.urls",
    ),
    path(
        "v1/",
        include("shigoto_q.kubernetes.urls"),
        name="shigoto_q.kubernetes.urls",
    ),
    path(
        "v1/",
        include("shigoto_q.products.urls"),
        name="shigoto_q.products.urls",
    ),
    path("v1/", include("shigoto_q.features.urls"), name="shigoto_q.features.urls"),
]
