import typing
from dataclasses import dataclass

from django.db.models import QuerySet
from django.core.paginator import Paginator

from rest.common.types import Page, Response


def fetch_and_paginate(
    func: typing.Callable,
    filters: dict,
    pagination: Page,
    serializer_func: typing.Union[dataclass, typing.Callable],
    is_serializer_dataclass=False,
):
    if filters:
        qs = func(filters)
    else:
        qs = func()
    if isinstance(qs, QuerySet):
        count = qs.count()
    else:
        count = len(qs)
    if int(pagination.size) < 1:
        if not is_serializer_dataclass:
            data = _handle_namedtuple_response(
                serializer_func=serializer_func, qs=qs, pagination=False
            )
        else:
            data = _handle_dataclass_serializer(
                serializer_func=serializer_func, qs=qs, pagination=False
            )

        return Response(
            data=data,
            count=count,
            page=pagination.page,
        )

    pages = Paginator(object_list=qs, per_page=pagination.size)
    if not is_serializer_dataclass:
        data = _handle_namedtuple_response(
            serializer_func=serializer_func, pages=pages, page=pagination.page
        )
    else:
        data = _handle_dataclass_serializer(
            serializer_func=serializer_func, pages=pages, page=pagination.page
        )
    return Response(
        data=data,
        count=count,
        page=pagination.page,
    )


def _handle_dataclass_serializer(
    serializer_func, page=None, pagination=True, qs=None, pages=None
):
    if pagination:
        return [serializer_func(obj).__dict__ for obj in pages.get_page(page)]
    else:
        return [serializer_func(obj).__dict__ for obj in qs]


def _handle_namedtuple_response(
    serializer_func, page=None, pagination=True, qs=None, pages=None
):
    if pagination:
        return [serializer_func(obj)._asdict() for obj in pages.get_page(page)]
    else:
        return [serializer_func(obj)._asdict() for obj in qs]
