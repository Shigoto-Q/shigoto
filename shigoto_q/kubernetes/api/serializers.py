from rest_framework import serializers

from rest.serializers import CamelCaseSerializer


class DockerImageSerializer(CamelCaseSerializer):
    image_name = serializers.CharField(required=False)
    last_push = serializers.CharField(required=False)
    tag = serializers.CharField(required=False)


class KubernetesDeployment(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    image_name = serializers.CharField(required=False)
    service_name = serializers.CharField(required=False)
    host = serializers.CharField(required=False)
