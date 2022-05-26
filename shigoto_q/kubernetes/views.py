from rest.views import ResourceView
from shigoto_q.kubernetes.api.serializers import (
    KubernetesDeployment,
    KubernetesNamespaceSerializer,
)
from shigoto_q.kubernetes.services import kubernetes
from shigoto_q.users.permissions import ProfessionalPlanPermission, PersonalPlanPermission, BusinessPlanPermission


class KubernetesDeployView(ResourceView):
    serializer_load_class = KubernetesDeployment
    serializer_dump_class = KubernetesDeployment
    permission_classes = [ProfessionalPlanPermission, PersonalPlanPermission]
    owner_check = True

    def execute(self, data):
        return kubernetes.create_kubernetes_deployment(data)


class KubernetesCreateNamespaceView(ResourceView):
    serializer_load_class = KubernetesNamespaceSerializer
    serializer_dump_class = KubernetesNamespaceSerializer
    permission_classes = [ProfessionalPlanPermission | PersonalPlanPermission | BusinessPlanPermission]
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
