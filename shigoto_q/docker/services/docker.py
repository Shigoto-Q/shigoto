import datetime
import logging

from django.db import transaction

from shigoto_q.docker import models as docker_models

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[DOCKER-SERVICES]"


def list_docker_images(filters: dict = None):
    data = []
    docker_images = docker_models.DockerImage.objects.filter(**filters)
    for image in docker_images:
        # image_details = DockerClient.get_image_details(image.image_name)
        # TODO Docker in docker to properly work.
        image_details = {
            "last_update": datetime.datetime.now(),
            "created_at": datetime.datetime.now(),
        }
        last_pushed_at = (
            datetime.datetime.now().astimezone() - image_details["last_update"]
        )
        data.append(
            dict(
                image_name=image.image_name,
                last_push_at=round(last_pushed_at.total_seconds() / 3600, 2),
                created_at=image_details["created_at"],
                tag="latest",
            )
        )
    return data


def get_total_docker_images() -> int:
    return docker_models.DockerImage.objects.count()


def create_docker_image(data):
    with transaction.atomic():
        image = docker_models.DockerImage.objects.create(**data)
        logger.info(f"{_LOG_PREFIX} Creating new docker image with data - {data}")
    return image.__dict__
