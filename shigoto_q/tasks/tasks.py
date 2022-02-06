import json
import time

import docker
import requests

from config import celery_app
from services.kubernetes import client as kubernetes_client
from services.internal_docker import services as docker_services


@celery_app.task()
def simple_http_operator(request_endpoint, headers=None, user=None, task_name=None):
    response = requests.get(request_endpoint, headers)
    try:
        time.sleep(5)
        return response.json()
    except json.decoder.JSONDecodeError:
        return response.text


@celery_app.task()
def kubernetes(repo_url, full_name, image_name, command, user, task_name):
    kubernetes_client.KubernetesService.create_job(
        task_name=task_name, image_name=image_name, command=command
    )


@celery_app.task()
def docker(image_name):
    # TODO Stream logs
    docker_instance = docker_services.get_docker_service(image_name)
    docker_instance.docker_image_pull()
    docker_instance.create_and_start_docker_container()
