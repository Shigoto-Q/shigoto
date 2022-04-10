import enum


class KubernetesEventType(enum.Enum):
    PENDING = "Pending"
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETE = "DELETE"
    SUCCEEDED = "Succeeded"


class KubernetesKindTypes(enum.Enum):
    DEPLOYMENT = "Deployment"
    SERVICE = "Service"
    INGRESS = "Ingress"


class KubernetesApiVersions(enum.Enum):
    APPS_API_VERSION = "apps/v1"
    API_VERSION = "v1"
    INGRESS_API_VERSION = "networking.k8s.io/v1"


LABELS = {
    "app": "deployment",
}
METADATA_NAME = "deployment"
API_VERSION = "apps/v1"
NAMESPACE = "default"
DEFAULT_PORT = 5678
DEFAULT_HOST = "shigo.to"
