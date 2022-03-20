import logging

from django.core import exceptions as django_exceptions
from rest_framework import exceptions as drf_exceptions

from rest.views.base import BaseView
from rest.serializers import ResourceListResponseSerializer
from rest.responses import OkResponse, BadResponse


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[REST-RESOURCE-LIST]"


class ResourceListView(BaseView):
    def get(self, request, *args, **kwargs):
        resource = self.fetch(self.get_data)
        data = self._process_post_response_data(resource)
        response = self._process_list_response(data)
        return OkResponse(response)

    def _process_post_response_data(self, resource):
        response_data = self.get_dump_serializer(data=resource, many=True,)
        response_data.is_valid(raise_exception=True)
        return response_data.data

    def _process_list_response(self, data):
        response = ResourceListResponseSerializer(
            data={"count": len(data), "data": data}
        )
        response.is_valid(raise_exception=True)
        return response.data

    def fetch(self, filters):
        """
        Method for GET requests, every GET view should implement fetch().
        Raises:
            NotImplementedError

        """
        raise NotImplementedError()
