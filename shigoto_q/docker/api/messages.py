import datetime

import typing


class DockerImage(
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
