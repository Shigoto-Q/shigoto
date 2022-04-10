import logging

import sentry_sdk

from services.kubernetes import client as kubernetes_client
from services.kubernetes import exceptions as kubernetes_exceptions

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[KUBERNETES-INTERNAL-SERVICE]"


def deploy(data):
    try:
        return kubernetes_client.KubernetesService.create_deployment_and_ingress(**data)
    except kubernetes_exceptions.KubernetesServiceError as e:
        logger.exception(
            f"{_LOG_PREFIX} Caught an error while trying to deploy to kubernetes: {str(e)}"
        )
        sentry_sdk.capture_message(str(e))
