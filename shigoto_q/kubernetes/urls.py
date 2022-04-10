from django.urls import path

from shigoto_q.kubernetes import views

app_name = "kubernetes"

urlpatterns = [
    path(
        "/kubernetes/deploy/",
        views.KubernetesDeployView.as_view(),
        name="shigoto_q.kubernetes.deploy",
    ),
]
