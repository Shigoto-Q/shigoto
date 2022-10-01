from rest.common.fetch import fetch_and_paginate
from rest.views import ResourceListView, ResourceView
from shigoto_q.docker.api import serializers
from shigoto_q.docker.services import docker as docker_services
from shigoto_q.docker.api.messages import DockerImage


class DockerImageListView(ResourceListView):
    serializer_dump_class = serializers.DockerImageSerializer
    serializer_load_class = serializers.DockerImageSerializer
    feature_flag = "ff02_docker"
    owner_check = True

    def fetch(self, filters, pagination):

        return fetch_and_paginate(
            func=docker_services.list_docker_images,
            filters=filters,
            pagination=pagination,
            serializer_func=DockerImage.from_dict,
            is_serializer_dataclass=True,
        )


class DockerImageCreateView(ResourceView):
    """
    View for creating, building images and pushing them to the docker registry.
    """

    http_method_names = ["post"]
    serializer_dump_class = serializers.DockerImageCreateDumpSerializer
    serializer_load_class = serializers.DockerImageCreateLoadSerializer
    owner_check = True

    def execute(self, data):
        return docker_services.create_docker_image(data=data)
