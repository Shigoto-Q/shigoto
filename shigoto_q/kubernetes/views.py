from rest.common.types import Page
from rest.views import ResourceView, ResourceListView
from rest.common.fetch import fetch_and_paginate
from shigoto_q.kubernetes.api.serializers import (
    KubernetesDeployment,
    KubernetesNamespaceSerializer,
    KubernetesNamespaceListSerializer,
    KubernetesDeploymentLoadSerializer,
    KubernetesServiceDumpSerializer,
    KubernetesServiceLoadSerializer,
)
from shigoto_q.kubernetes.services import kubernetes
from shigoto_q.kubernetes.services import messages as kubernetes_messages
from shigoto_q.users.permissions import (
    ProfessionalPlanPermission,
    PersonalPlanPermission,
    BusinessPlanPermission,
)


class KubernetesDeployView(ResourceView):
    serializer_load_class = KubernetesDeploymentLoadSerializer
    serializer_dump_class = KubernetesDeployment
    permission_classes = [ProfessionalPlanPermission | PersonalPlanPermission | BusinessPlanPermission]
    owner_check = True

    def execute(self, data):
        return kubernetes.create_kubernetes_deployment(data)


class KubernetesCreateNamespaceView(ResourceView):
    serializer_load_class = KubernetesNamespaceSerializer
    serializer_dump_class = KubernetesNamespaceSerializer
    permission_classes = [
        ProfessionalPlanPermission | PersonalPlanPermission | BusinessPlanPermission
    ]
    owner_check = True

    def execute(self, data):
        return kubernetes.create_namespace(
            name=data.get("name"),
            user_id=data.get("user_id"),
        )


class KubernetesNamespaceDeleteView(ResourceView):
    serializer_load_class = KubernetesNamespaceSerializer
    serializer_dump_class = KubernetesNamespaceSerializer
    owner_check = True

    def execute(self, data):
        return kubernetes.delete_namespace(
            name=data.get("name"),
            user_id=data.get("user_id"),
        )


class KubernetesNamespaceList(ResourceListView):
    serializer_load_class = KubernetesNamespaceListSerializer
    serializer_dump_class = KubernetesNamespaceListSerializer
    owner_check = True

    def fetch(self, filters: dict, pagination: Page):
        return fetch_and_paginate(
            func=kubernetes.list_user_namespaces,
            filters=filters,
            pagination=pagination,
            serializer_func=kubernetes_messages.Namespace.from_model,
        )


class KubernetesServiceCreateView(ResourceView):
    serializer_load_class = KubernetesServiceLoadSerializer
    serializer_dump_class = KubernetesServiceDumpSerializer
    permission_classes = [ProfessionalPlanPermission | PersonalPlanPermission | BusinessPlanPermission]
    owner_check = True

    def execute(self, data):
        return kubernetes.create_kubernetes_service(data=data)
