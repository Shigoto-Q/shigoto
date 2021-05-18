import json
import time

import requests

from config import celery_app


@celery_app.task()
def custom_endpoint(request_endpoint, headers=None, user=None, task_name=None):
    response = requests.get(request_endpoint, headers)
    try:
        time.sleep(5)
        return response.json()
    except json.decoder.JSONDecodeError:
        return response.text
