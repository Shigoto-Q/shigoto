from django.urls import include, path

app_name = "shigoto"

urlpatterns = [
    path("v1/", include("shigoto_q.tasks.urls"), name="shigoto_q.tasks.urls"),
    path("v1/", include("shigoto_q.users.urls"), name="shigoto_q.users.urls"),
    path("v1/", include("shigoto_q.github.urls"), name="shigoto_q.github.urls"),
    path("v1/", include("shigoto_q.docker.urls"), name="shigoto_q.docker.urls"),
]
