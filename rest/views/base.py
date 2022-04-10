import collections
import json
import logging

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest.common.types import Page
from rest.serializers import BadResponseSerializer

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[REST]"


class BaseView(APIView):
    """
    Custom api view that processes the request body and the response.
        serializer_dump_class: Serializer class that is used to parse response
        serializer_load_class: Serializer to parse request params
        exception_serializer: Default serializer for 400 error
        owner_check: Check whether the owner of the request matches the resource owner
    """

    serializer_dump_class = None
    serializer_load_class = None
    exception_serializer = BadResponseSerializer
    owner_check = None
    permission_classes = [IsAuthenticated]
    request_param = "pk"
    post_data = {}
    get_data = {}
    page = None
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    def __init__(self, *args, **kwargs):
        self._request_param = None
        self._is_one_resource = []
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self._process_request_pk_param(kwargs)
        self._process_post_params()
        return super().dispatch(request, *args, **kwargs)

    def _ownership_check(self, data: collections.OrderedDict, fields):
        if self.owner_check:
            data["user_id"] = self.request.user.id
        return data

    def _process_request_data(self):
        load_serializer = self.get_load_serializer(data=self.post_data)
        load_serializer.is_valid(raise_exception=True)
        data = load_serializer.validated_data
        data = self._ownership_check(data, load_serializer.fields)
        return data

    def _process_post_response_data(self, resource):
        response_data = self.get_dump_serializer(data=resource)
        response_data.is_valid(raise_exception=True)
        return response_data.data

    def get_load_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_load_class()
        return serializer_class(*args, **kwargs)

    def get_exception_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_exception_class()
        return serializer_class(*args, **kwargs)

    def get_dump_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_dump_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_dump_class(self):
        assert self.serializer_dump_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )
        return self.serializer_dump_class

    def get_serializer_load_class(self):
        assert self.serializer_load_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )
        return self.serializer_load_class

    def get_serializer_exception_class(self):
        assert (
            self.exception_serializer is BadResponseSerializer
        ), "You should not change exception serializer class!"
        return self.exception_serializer

    def create_instance(self, request):
        return self.post(request)

    def _process_post_params(self):
        content_type = self.request.headers.get("Content-Type", "")
        if "application/x-www-urlencoded" in content_type:
            self.post_data = self.request.POST
        self.post_data = json.loads(self.request.body or "{}")

    def _process_request_pk_param(self, kwargs):
        self._request_param = kwargs.pop(self.request_param, None)

    def _process_get_params(self):
        self.get_data = self.request.GET.dict()
        self.page = Page(
            page=self.get_data.get("page", 1),
            size=self.get_data.get("perPage", 10),
        )
        load_serializer = self.get_load_serializer(data=self.post_data)
        load_serializer.is_valid(raise_exception=True)
        data = load_serializer.validated_data
        data = self._ownership_check(data, load_serializer.fields)
        self.get_data = data

    def _process_bad_response(self, exception_message):
        exception_message = dict(message=exception_message)
        response = self.get_exception_serializer(data=exception_message)
        response.is_valid()
        return response.data
