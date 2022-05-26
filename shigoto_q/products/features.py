import enum

from django.conf import settings


class DockerFeatureEnum(enum.Enum):
    IMAGE_BUILD = "Image building"
    IMAGE_PUSH = "Image push to docker registry"


class KubernetesFeatureEnum(enum.Enum):
    DEPLOYMENT = "Kubernetes deployments"
    INGRESS = "Kubernetes Ingress"
    NAMESPACE = "Namespace"


class TaskFeatureEnum(enum.Enum):
    SIMPLE_HTTP_OPERATOR = "Simple HTTP Operator cron jobs"
    KUBERNETES_JOB = "Kubernetes cron job"
    DOCKER_JOB = "Docker job"
    SCHEDULER = "Scheduler"


PERSONAL_PLAN_DEPLOYMENT_LIMITS = 1
PROFESSIONAL_PLAN_DEPLOYMENT_LIMITS = 5
BUSINESS_PLAN_DEPLOYMENT_LIMITS = 100


PERSONAL_PLAN_NAMESPACES = 1
PROFESSIONAL_PLAN_NAMESPACES = 5
BUSINESS_PLAN_NAMESPACES = 1


PERSONAL_PLAN_LIMITS = (
    (KubernetesFeatureEnum.DEPLOYMENT.value, PERSONAL_PLAN_DEPLOYMENT_LIMITS),
    (KubernetesFeatureEnum.NAMESPACE.value, PERSONAL_PLAN_NAMESPACES),
    (DockerFeatureEnum.IMAGE_PUSH.value, None),
    (DockerFeatureEnum.IMAGE_BUILD.value, None),
    (TaskFeatureEnum.SIMPLE_HTTP_OPERATOR, None),
    (TaskFeatureEnum.KUBERNETES_JOB, False),
    (TaskFeatureEnum.DOCKER_JOB, None),
)

PROFESSIONAL_PLAN_LIMITS = (
    (KubernetesFeatureEnum.DEPLOYMENT.value, PROFESSIONAL_PLAN_DEPLOYMENT_LIMITS),
    (KubernetesFeatureEnum.NAMESPACE.value, PROFESSIONAL_PLAN_NAMESPACES),
    (DockerFeatureEnum.IMAGE_PUSH.value, None),
    (DockerFeatureEnum.IMAGE_BUILD.value, None),
    (TaskFeatureEnum.SIMPLE_HTTP_OPERATOR, None),
    (TaskFeatureEnum.KUBERNETES_JOB, 10),
    (TaskFeatureEnum.DOCKER_JOB, None),
)

BUSINESS_PLAN_LIMITS = (
    (KubernetesFeatureEnum.DEPLOYMENT.value, BUSINESS_PLAN_DEPLOYMENT_LIMITS),
    (KubernetesFeatureEnum.NAMESPACE.value, BUSINESS_PLAN_NAMESPACES),
    (DockerFeatureEnum.IMAGE_PUSH.value, None),
    (DockerFeatureEnum.IMAGE_BUILD.value, None),
    (TaskFeatureEnum.SIMPLE_HTTP_OPERATOR, None),
    (TaskFeatureEnum.KUBERNETES_JOB, 100),
    (TaskFeatureEnum.DOCKER_JOB, None),
)


def get_limits_by_plan(plan_id):
    _mapping = {
        settings.PERSONAL_PLAN: PERSONAL_PLAN_LIMITS,
        settings.PROFESSIONAL_PLAN: PROFESSIONAL_PLAN_LIMITS,
        settings.BUSINESS_PLAN: BUSINESS_PLAN_LIMITS,
    }

    return _mapping.get(plan_id)
