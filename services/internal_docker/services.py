import datetime
import json
import logging

import docker
from django.conf import settings

from services.internal_docker.exceptions import (
    DockerContainerNotFound,
    DockerImageNotFound,
)

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[DOCKER-SERVICE]"

client = docker.APIClient(base_url=f"tcp://{settings.DIND_HOST}:{settings.DIND_PORT}")


class DockerService:
    def __init__(self, client: docker.APIClient, image_name: str):
        self.container = None
        self.image_name = image_name
        self.client = client

    def docker_image_pull(self, stream: bool = True) -> dict:
        logger.info(
            f"{_LOG_PREFIX} Pulling Image(name={self.image_name}) from docker hub"
        )
        if stream:
            for line in self.client.pull(self.image_name, stream=stream, decode=True):
                yield json.dumps(line, indent=4)
        else:
            return self.client.pull(self.image_name, decode=True)

    def create_and_start_docker_container(self) -> None:
        try:
            self.container = self.client.create_container(image=self.image_name)
            self.client.start(self.container)
            logger.info(
                f"{_LOG_PREFIX} Container(id={self.container.get('Id')} has been created and started"
            )
        except Exception as e:
            raise DockerImageNotFound(str(e))

    def get_container_logs(
        self, stream_output: bool = False, current_logs: bool = True
    ) -> dict:
        stream_message = {}
        current_logs_datetime = None
        if current_logs:
            current_logs_datetime = datetime.datetime.now()
        try:
            if stream_output:
                for line in self.client.logs(
                    self.container, stream=stream_output, since=current_logs_datetime
                ):
                    stream_message["message"] = line
                    yield stream_message
            else:
                stream_message["message"] = self.client.logs(
                    self.container, since=current_logs_datetime
                )
                return stream_message

        except Exception as e:
            raise DockerContainerNotFound(str(e))


def get_docker_service(image_name: str) -> DockerService:
    return DockerService(client, image_name)
