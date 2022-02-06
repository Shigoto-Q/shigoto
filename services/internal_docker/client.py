import requests

from django.conf import settings


class DockerImageService:
    @classmethod
    def create_image(
        cls, repo_url: str, full_name: str, image_name: str
    ) -> requests.Response:
        return requests.post(
            settings.DOCKER_IMAGE_SERVICE,
            json={
                "repo_url": repo_url,
                "full_name": full_name,
                "image_name": image_name,
            },
        )
