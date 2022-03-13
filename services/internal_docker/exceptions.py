class DockerServiceError(Exception):
    """
    Base exception class for internal docker service
    """

    pass


class DockerContainerNotFound(DockerServiceError):
    pass


class DockerImageNotFound(DockerServiceError):
    pass
