import json
import time

import requests

from config import celery_app
from services import kubernetes as kube_service


@celery_app.task()
def custom_endpoint(request_endpoint, headers=None, user=None, task_name=None):
    response = requests.get(request_endpoint, headers)
    try:
        time.sleep(5)
        return response.json()
    except json.decoder.JSONDecodeError:
        return response.text


@celery_app.task()
def k8s_job(
    repo_url,
    full_name,
    image_name,
    command,
    user=None,
    task_name=None,
):
    kubernetes = kube_service.KubernetesService(task_name, image_name, command)
    kubernetes.create_job()
    kubernetes.watch_job()
