import typing

from shigoto_q.kubernetes import models as kubernetes_models


class Deployment(
    typing.NamedTuple(
        "Deployment",
        [
            ("name", str),
            ("image", str),
            ("external_id", str),
            ("kind", int),
        ],
    )
):
    @classmethod
    def from_model(cls, deployment: kubernetes_models.Deployment):
        return cls(
            name=deployment.name,
            image=deployment.image.name,
            external_id=deployment.external_id,
            kind=deployment.kind,
        )


class Namespace(
    typing.NamedTuple(
        "Namespace",
        [
            ("name", str),
            ("id", int),
        ],
    )
):
    @classmethod
    def from_model(cls, namespace: kubernetes_models.Namespace):
        return cls(
            name=namespace.name,
            id=namespace.id,
        )
