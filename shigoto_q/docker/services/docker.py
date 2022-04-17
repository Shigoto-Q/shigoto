import datetime

from services.docker.client import DockerClient

from shigoto_q.docker import models as docker_models


def list_docker_images(filters: dict = None):
    data = []
    docker_images = docker_models.DockerImage.objects.filter(**filters)
    for image in docker_images:
        image_details = DockerClient.get_image_details(image.image_name)
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
