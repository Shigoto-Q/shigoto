import secrets

from django.db import models


def generate_secret():
    return secrets.token_urlsafe()


class Deployment(models.Model):
    external_id = models.CharField(
        max_length=512,
        default=generate_secret,
        unique=True,
    )
    kind = models.IntegerField()
    image = models.ForeignKey("docker.DockerImage", on_delete=models.PROTECT)
    name = models.CharField(max_length=512)
    metadata = models.TextField(null=True)
