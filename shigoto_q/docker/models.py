import secrets

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def generate_secret():
    return secrets.token_urlsafe()


class DockerImage(models.Model):
    repository = models.CharField(
        max_length=255, verbose_name=_("Github repository url")
    )

    name = models.CharField(max_length=255, verbose_name=_("Github repository name"))

    image_name = models.CharField(
        unique=True,
        verbose_name=_("Image name"),
        help_text=_("Name of the Docker image inside user namespace"),
        max_length=255,
    )

    command = models.CharField(
        max_length=255,
        help_text=_("Command to execute after image startup."),
        verbose_name=_("Command to execute"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name=_("User"),
    )
    secret_key = models.CharField(
        max_length=512,
        default=generate_secret,
        null=True,
        blank=True,
        unique=True,
    )
