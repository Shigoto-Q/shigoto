from rest.views import ResourceListView
from shigoto_q.docker.api import serializers
from shigoto_q.docker.services import docker as docker_services


class DockerImageListView(ResourceListView):
    serializer_dump_class = serializers.DockerImageSerializer
    serializer_load_class = serializers.DockerImageSerializer
    owner_check = True

    def fetch(self, filters):
        return docker_services.list_docker_images(filters=filters)
