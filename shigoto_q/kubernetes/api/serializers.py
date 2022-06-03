from rest_framework import serializers

from rest.serializers import CamelCaseSerializer


class DockerImageSerializer(CamelCaseSerializer):
    image_name = serializers.CharField(required=False)
    last_push = serializers.CharField(required=False)
    tag = serializers.CharField(required=False)


class KubernetesDeployment(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)


class KubernetesDeploymentLoadSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    namespace = serializers.CharField(required=False)
    port = serializers.IntegerField(required=False)


class KubernetesNamespaceSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=True)


class KubernetesDeploymentListSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    external_id = serializers.UUIDField(required=False)
    kind = serializers.IntegerField(required=False)


class KubernetesNamespaceListSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)


class KubernetesServiceLoadSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    port = serializers.IntegerField(required=False)
    target_port = serializers.IntegerField(required=False)
    namespace = serializers.CharField(required=False)


class KubernetesServiceDumpSerializer(CamelCaseSerializer):
    name = serializers.CharField(required=False)
    port = serializers.IntegerField(required=False)
    target_port = serializers.IntegerField(required=False)
    namespace = serializers.CharField(required=False)
