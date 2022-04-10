from rest.views import ResourceView
from shigoto_q.kubernetes.api.serializers import KubernetesDeployment
from shigoto_q.kubernetes.services import kubernetes


class KubernetesDeployView(ResourceView):
    serializer_load_class = KubernetesDeployment
    serializer_dump_class = KubernetesDeployment
    owner_check = True

    def execute(self, data):
        return kubernetes.deploy(data)
