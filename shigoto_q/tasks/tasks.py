import requests

from config import celery_app


@celery_app.task()
def custom_endpoint(request_endpoint, headers=None):
    response = requests.get(request_endpoint, headers)
    return response.json()
