from rest_framework import status
from rest_framework.response import Response


class OkResponse(Response):
    def __init__(
        self,
        data=None,
        static_status=status.HTTP_200_OK,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        super().__init__(
            data=data,
            status=static_status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )


class BadResponse(Response):
    def __init__(
        self,
        data=None,
        static_status=status.HTTP_400_BAD_REQUEST,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        super().__init__(
            data=data,
            status=static_status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
