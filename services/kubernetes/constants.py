import enum


class KubernetesEventType(enum.Enum):
    PENDING = "Pending"
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETE = "DELETE"
    SUCCEEDED = "Succeeded"
