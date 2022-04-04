import datetime
import typing
from dataclasses import dataclass


class OldDockerImage(
    typing.NamedTuple(
        "UserTask",
        [
            ("image_name", str),
            ("last_push_at", str),
            ("created_at", datetime.datetime),
            ("tag", str),
        ],
    )
):
    pass


@dataclass
class DockerImage:
    image_name: str
    last_push_at: str
    created_at: datetime.datetime
    tag: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            image_name=data["image_name"],
            last_push_at=data["last_push_at"],
            created_at=data["created_at"],
            tag=data["tag"],
        )
