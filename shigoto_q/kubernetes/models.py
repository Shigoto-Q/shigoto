import secrets
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from shigoto_q.kubernetes.enums import KubernetesKinds, KubernetesServiceTypes


User = get_user_model()


def generate_secret():
    return secrets.token_urlsafe()


class Deployment(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    kind = models.PositiveSmallIntegerField(default=KubernetesKinds.DEPLOYMENT)
    image = models.ForeignKey("docker.DockerImage", on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    metadata = models.TextField(null=True)
    port = models.IntegerField(default=0)
    yaml = models.TextField(null=True)  # TODO: Implement YamlField
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )


class Service(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.PositiveSmallIntegerField(choices=KubernetesServiceTypes.choices)
    name = models.CharField(max_length=512)
    metadata = models.TextField(null=True)
    port = models.IntegerField()
    target_port = models.IntegerField()
    yaml = models.TextField(null=True)  # TODO: Implement YamlField
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )


class Ingress(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=256)
    host = models.CharField(max_length=256)
    metadata = models.TextField(null=True)
    path = models.CharField(max_length=100)
    path_type = models.CharField(max_length=100)
    yaml = models.TextField(null=True)  # TODO: Implement YamlField
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )


class Namespace(models.Model):
    name = models.CharField(max_length=512, default="default")
    deployments = models.ManyToManyField(Deployment)
    services = models.ManyToManyField(Service)
    ingress = models.OneToOneField(Ingress, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )


class Config(models.Model):
    file = models.FileField(upload_to="media/keyfiles/configs/")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
