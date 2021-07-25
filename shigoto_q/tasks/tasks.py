import json
import time

import requests

from config import celery_app
from services.kubernetes import kube_service


@celery_app.task()
def custom_endpoint(request_endpoint, headers=None, user=None, task_name=None):
    response = requests.get(request_endpoint, headers)
    try:
        time.sleep(5)
        return response.json()
    except json.decoder.JSONDecodeError:
        return response.text


@celery_app.task()
def k8s_job(repo_url, full_name, image_name, command, user=None, task_name=None):
    return kube_service.run_job(task_name, image_name, command)
