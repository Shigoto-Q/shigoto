import json
import time

import docker
import requests

from config import celery_app
from services.kubernetes import client as kubernetes_client


@celery_app.task()
def simple_http_operator(url, headers=None, user_id=None, task_name=None):
    response = requests.get(url, headers)
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
