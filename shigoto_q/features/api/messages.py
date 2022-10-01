import typing


class URL(
    typing.NamedTuple(
        "URL",
        [
            ("name", str),
            ("url", str),
        ],
    )
):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            url=data["url"],
        )
