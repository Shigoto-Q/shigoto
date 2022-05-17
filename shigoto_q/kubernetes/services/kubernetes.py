import logging
import json

import sentry_sdk

from shigoto_q.integrations import services as integration_services
from shigoto_q.integrations import constants as integration_constants
from services.kubernetes import client as kubernetes_client
from services.kubernetes import exceptions as kubernetes_exceptions
from shigoto_q.kubernetes.models import Deployment
from shigoto_q.docker.models import DockerImage

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[KUBERNETES-INTERNAL-SERVICE]"


def create_kubernetes_deployment(data: dict):
    try:
        logger.info(f"{_LOG_PREFIX} Creating new Deployment({data}).")
        image = DockerImage.objects.filter(image_name=data.get('image')).first()
        if image is None:
            raise Exception('Image does not exist.')
        resp = kubernetes_client.KubernetesService.create_deployment(**data)
        data['image'] = image
        deployment = Deployment.objects.create(**data)
        deployment.metadata = resp.metadata
        deployment.yaml = resp
        deployment.save()
        observer = integration_services.get_observer_for_event(
            user_id=data.get('user_id'),
            event=integration_constants.Event.DEPLOYMENT.value,
        )
        if observer is not None:
            observer.execute(
                event_type=integration_constants.Event.DEPLOYMENT,
                description=f"Deploying image {data['image'].name}"
            )
    except kubernetes_exceptions.KubernetesServiceError as e:
        keyword = 'HTTP response body:'
        _, _, parsed_exception = str(e).partition(keyword)
        msg = json.loads(parsed_exception)['details']['causes'][0]['message']
        logger.exception(
            f"{_LOG_PREFIX} Caught an error while trying to deploy to kubernetes: {msg}."
        )
        sentry_sdk.capture_message(msg)
        raise Exception(msg)


def get_total_deployments() -> int:
    return Deployment.objects.count()
