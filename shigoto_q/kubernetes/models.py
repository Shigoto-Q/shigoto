import secrets
import uuid

from django.conf import settings
from django.db import models

from shigoto_q.kubernetes.enums import KubernetesKinds, KubernetesServiceTypes


def generate_secret():
    return secrets.token_urlsafe()


class Deployment(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    kind = models.PositiveSmallIntegerField(default=KubernetesKinds.DEPLOYMENT)
    image = models.ForeignKey("docker.DockerImage", on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    metadata = models.TextField(null=True)
    yaml = models.TextField(null=True)  # TODO: Implement YamlField
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


class Service(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.PositiveSmallIntegerField(choices=KubernetesServiceTypes.choices)
    name = models.CharField(max_length=512)
    namespace = models.CharField(max_length=256)
    metadata = models.TextField(null=True)
    port = models.IntegerField()
    target_port = models.IntegerField()
    yaml = models.TextField(null=True)  # TODO: Implement YamlField


class Ingress(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=256)
    host = models.CharField(max_length=256)
    metadata = models.TextField(null=True)
    path = models.CharField(max_length=100)
    path_type = models.CharField(max_length=100)
    yaml = models.TextField(null=True)  # TODO: Implement YamlField
