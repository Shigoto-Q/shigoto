import typing


class Task(typing.NamedTuple("Task", [("id", int), ("name", str), ("value", str)])):
    pass
