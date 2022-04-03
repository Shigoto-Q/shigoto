from rest_framework import serializers

from rest.serializers import CamelCaseSerializer


class DockerImageSerializer(CamelCaseSerializer):
    image_name = serializers.CharField(required=False)
    last_push_at = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    tag = serializers.CharField(required=False)
