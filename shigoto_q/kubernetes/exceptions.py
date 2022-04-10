class KubernetesBaseError(Exception):
    pass


class KubernetesNamespaceDoesNotExist(KubernetesBaseError):
    pass


class KubernetesServiceNotFound(KubernetesBaseError):
    pass
