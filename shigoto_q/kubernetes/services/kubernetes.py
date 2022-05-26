import logging
import json

from django.db import transaction
from django.contrib.auth import get_user_model
import sentry_sdk

from shigoto_q.docker.models import DockerImage
from shigoto_q.integrations import services as integration_services
from shigoto_q.integrations import constants as integration_constants
from services.kubernetes import client as kubernetes_client
from services.kubernetes import exceptions as kubernetes_exceptions
from shigoto_q.users.decorators import subscription_check
from shigoto_q.kubernetes.models import Deployment, Namespace
from shigoto_q.products import features as product_features

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[KUBERNETES-INTERNAL-SERVICE]"


User = get_user_model()


def create_kubernetes_deployment(data: dict):
    with transaction.atomic():
        try:
            namespace = data.pop("namespace")
            try:
                namespace = Namespace.objects.get(name=namespace)
            except Namespace.DoesNotExist:
                # TODO: Add Kubernetes service exceptions.
                raise Exception("Namespace not found.")

            logger.info(f"{_LOG_PREFIX} Creating new Deployment({data}).")
            image = DockerImage.objects.filter(image_name=data.get("image")).first()

            if image is None:
                raise Exception("Image does not exist.")
            resp = kubernetes_client.KubernetesService.create_deployment(**data)
            data["image"] = image
            deployment = Deployment.objects.create(**data)
            deployment.metadata = resp.metadata
            deployment.yaml = resp
            deployment.save()
            namespace.deployments.add(deployment)
            observer = integration_services.get_observer_for_event(
                user_id=data.get("user_id"),
                event=integration_constants.Event.DEPLOYMENT.value,
            )
            if observer is not None:
                observer.execute(
                    event_type=integration_constants.Event.DEPLOYMENT,
                    description=f"Deploying image {data['image'].name}",
                )
        except kubernetes_exceptions.KubernetesServiceError as e:
            keyword = "HTTP response body:"
            _, _, parsed_exception = str(e).partition(keyword)
            msg = json.loads(parsed_exception)["details"]["causes"][0]["message"]
            logger.exception(
                f"{_LOG_PREFIX} Caught an error while trying to deploy to kubernetes: {msg}."
            )
            sentry_sdk.capture_message(msg)
            raise Exception(msg)


def get_total_deployments() -> int:
    return Deployment.objects.count()


@subscription_check(
    prerequisites=[product_features.KubernetesFeatureEnum.NAMESPACE.value]
)
def create_namespace(name: str, user_id: int) -> dict:
    client = kubernetes_client.KubernetesService()
    user = User.objects.get(id=user_id)
    with transaction.atomic():
        namespace = Namespace.objects.create(name=name, user_id=user_id).__dict__
        client.create_namespace(name=name)
        user.total_active_namespaces += 1
        user.save()
        logger.info(
            f"{_LOG_PREFIX} Creating Namespace(name={name}) for User(id={user_id})."
        )
        return namespace


def delete_namespace(name: str, user_id: int):
    client = kubernetes_client.KubernetesService()
    user = User.objects.get(id=user_id)
    with transaction.atomic():
        namespace = Namespace.objects.get(name=name, user_id=user_id)
        namespace.delete()
        client.delete_namespace(namespace.name)
        user.total_active_namespaces -= 1
        logger.info(
            f"{_LOG_PREFIX} Deleting Namespace(name={name}) for User(id={user_id})."
        )
