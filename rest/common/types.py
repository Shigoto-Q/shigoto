from dataclasses import dataclass


@dataclass
class Page:
    page: int
    size: int


@dataclass
class Response:
    data: list
    count: int
    page: int
