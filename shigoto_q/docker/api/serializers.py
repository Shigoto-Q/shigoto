from rest_framework import serializers

from rest.serializers import CamelCaseSerializer


class DockerImageSerializer(CamelCaseSerializer):
    image_name = serializers.CharField(required=False)
    last_push_at = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    tag = serializers.CharField(required=False)


class DockerImageCreateDumpSerializer(CamelCaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    repository = serializers.CharField()
    image_name = serializers.CharField()
    command = serializers.CharField()
    user_id = serializers.IntegerField(required=False)
    secret_key = serializers.CharField(required=False)


class DockerImageCreateLoadSerializer(CamelCaseSerializer):
    name = serializers.CharField()
    repository = serializers.CharField()
    image_name = serializers.CharField()
    command = serializers.CharField()
    user_id = serializers.IntegerField(required=False)
