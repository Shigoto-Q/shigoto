import logging

from django.db import transaction
from django.contrib.auth import get_user_model
import sentry_sdk

from shigoto_q.docker.models import DockerImage
from shigoto_q.integrations import services as integration_services
from shigoto_q.integrations import constants as integration_constants
from services.kubernetes import client as kubernetes_client
from services.kubernetes import exceptions as kubernetes_exceptions
from shigoto_q.users.decorators import subscription_check
from shigoto_q.kubernetes.models import Deployment, Namespace, Service
from shigoto_q.kubernetes import exceptions as kubernetes_exceptions
from shigoto_q.kubernetes import enums as kubernetes_enums
from shigoto_q.products import features as product_features

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[KUBERNETES-INTERNAL-SERVICE]"

User = get_user_model()


@subscription_check(
    prerequisites=[product_features.KubernetesFeatureEnum.DEPLOYMENT.value]
)
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
            data["image"] = image
            deployment = Deployment.objects.create(**data)
            namespace.deployments.add(deployment)
            observer = integration_services.get_observer_for_event(
                user_id=data.get("user_id"),
                event=integration_constants.Event.DEPLOYMENT.value,
            )
            data["namespace"] = namespace.name
            data["image"] = image.image_name
            resp = kubernetes_client.KubernetesService.create_deployment(**data)
            deployment.metadata = resp.metadata
            deployment.yaml = resp
            deployment.save()
            if observer is not None:
                observer.execute(
                    event_type=integration_constants.Event.DEPLOYMENT,
                    description=f"Deploying image {data['image'].name}",
                )
        except kubernetes_exceptions.KubernetesServiceError as e:
            # TODO: Create kubernetes client exception handler
            logger.exception(
                f"{_LOG_PREFIX} Caught an error while trying to deploy to kubernetes: {e}."
            )
            sentry_sdk.capture_message(e)
            raise Exception(e)


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
        user.save()
        logger.info(
            f"{_LOG_PREFIX} Deleting Namespace(name={name}) for User(id={user_id})."
        )


def list_user_namespaces(
    filters: dict = None,
    ordering: str = None,
) -> list:
    return Namespace.objects.filter(**filters).order_by(ordering if ordering else "id")


def create_kubernetes_service(data):
    client = kubernetes_client.KubernetesService()
    namespace = data.pop("namespace")
    try:
        namespace = Namespace.objects.get(name=namespace)
    except Namespace.DoesNotExist:
        raise kubernetes_exceptions.KubernetesNamespaceDoesNotExist(
            "Namespace not found."
        )
    observer = integration_services.get_observer_for_event(
        user_id=data.get("user_id"),
        event=integration_constants.Event.SERVICE.value,
    )
    copied_data = data.copy()
    with transaction.atomic():
        copied_data["type"] = kubernetes_enums.KubernetesServiceTypes.CLUSTER_IP.value
        service = Service.objects.create(**copied_data)
        created_service = client.create_service(
            service_name=data.get("name"),
            port=data.get("port"),
            target_port=data.get("target_port"),
            namespace=namespace.name,
            user_id=data.get("user_id"),
        )
        service.metadata = created_service.metadata
        service.yaml = created_service
        service.save()
        namespace.services.add(service)

        if observer is not None:
            observer.execute(
                event_type=integration_constants.Event.DEPLOYMENT,
                description=f"Create service",
            )


def delete_deployment(data: dict):
    client = kubernetes_client.KubernetesService()
    deployment = Deployment.objects.get(id=data.get("id"), user_id=data.get("user_id"))
    namespace = deployment.namespace_set.filter(id=data.get("namespace_id"))
    with transaction.atomic():
        client.delete_deployment(
            name=deployment.name,
            namespace=namespace.name,
        )
        namespace.deployments.remove(deployment)
        deployment.delete()
        logger.info(
            f'{_LOG_PREFIX} User(id={data.get("user_id")}) is deleting kubernetes deployment(id={deployment.id}).'
        )


def delete_service(data: dict):
    client = kubernetes_client.KubernetesService()
    service = Service.objects.get(id=data.get("id"), user_id=data.get("user_id"))
    namespace = service.namespace_set.filter(id=data.get("namespace_id")).first()
    with transaction.atomic():
        client.delete_service(service.name, namespace.name)
        namespace.services.remove(service)
        service.delete()
        logger.info(
            f'{_LOG_PREFIX} User(id={data.get("user_id")}) is deleting kubernetes service(id={service.id}).'
        )
