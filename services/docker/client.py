import json
import logging

from django.utils.dateparse import parse_datetime

import docker
from django.conf import settings


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[DOCKER-SERVICE]"
_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DockerClient:
    try:
        client = docker.APIClient(
            base_url=f"tcp://{settings.DIND_HOST}:{settings.DIND_PORT}"
        )
    except Exception:
        logger.exception(
            f"{_LOG_PREFIX} Caught exception while trying to initialize docker client."
        )

    @classmethod
    def build_image(cls, internal_path: str, image_tag: str):
        logger.info(f"{_LOG_PREFIX} Building new docker Image(tag={image_tag}).")
        for resp in cls.client.build(
            path=internal_path,
            tag=settings.DOCKER_TAG_PREFIX + image_tag,
        ):
            yield resp

    @classmethod
    def push_image(cls, image_tag: str):
        logger.info(f"{_LOG_PREFIX} Pushing new Image(tag={image_tag}).")
        for resp in cls.client.push(image_tag, stream=True, decode=True):
            yield resp

    @classmethod
    def docker_image_pull(cls, image_tag: str, stream: bool = True) -> dict:
        logger.info(f"{_LOG_PREFIX} Pulling Image(name={image_tag}) from docker hub")
        if stream:
            for line in cls.client.pull(image_tag, stream=stream, decode=True):
                yield json.dumps(line, indent=4)
        else:
            return cls.client.pull(cls.image_name, decode=True)

    @classmethod
    def build_and_push_image(cls, internal_path: str, image_tag: str):
        """
        Build and push image to docker hub, response streaming not allowed in this case

        Args:
            internal_path (str)
            image_tag (str)

        Returns:
            None
        """
        for _ in cls.build_image(internal_path=internal_path, image_tag=image_tag):
            pass
        for _ in cls.push_image(image_tag=image_tag):
            pass

    @classmethod
    def get_image_details(cls, image_name):
        image = cls.client.inspect_image(f"shigoto/{image_name}")
        return dict(
            last_update=parse_datetime(image["Metadata"]["LastTagTime"]),
            created_at=parse_datetime(image["Created"]),
        )

    @classmethod
    def delete_docker_image(cls, image_name):
        pass
