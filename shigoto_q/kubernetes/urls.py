from django.urls import path

from shigoto_q.kubernetes import views

app_name = "kubernetes"

urlpatterns = [
    path(
        "kubernetes/deploy/",
        views.KubernetesDeployView.as_view(),
        name="kubernetes.deploy",
    ),
    path(
        "kubernetes/namespace/create/",
        views.KubernetesCreateNamespaceView.as_view(),
        name="kubernetes.namespace.create",
    ),
    path(
        "kubernetes/namespace/delete/",
        views.KubernetesNamespaceDeleteView.as_view(),
        name="kubernetes.namespace.delete",
    ),
    path(
        "kubernetes/namespace/list/",
        views.KubernetesNamespaceList.as_view(),
        name="kubernetes.namespace.list",
    ),
    path(
        "kubernetes/service/create/",
        views.KubernetesServiceCreateView.as_view(),
        name="kubernetes.service.create",
    ),
]
