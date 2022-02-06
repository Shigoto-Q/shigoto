class KubernetesServiceError(Exception):
    """
    Base kubernetes service error
    """

    pass


class KubernetesJobNotFoundError(KubernetesServiceError):
    pass
