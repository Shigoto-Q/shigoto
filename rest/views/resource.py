import logging

from django.core import exceptions as django_exceptions
from rest_framework import exceptions as drf_exceptions

from rest.responses import BadResponse, NoContentResponse, OkResponse
from rest.views.base import BaseView

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[REST-RESOURCE]"


class ResourceView(BaseView):
    def get(self, request, *args, **kwargs):
        try:
            self._process_get_params()
            resource = self.fetch_one(self._request_param)
            data = self._process_post_response_data(resource)
            return OkResponse(data)
        except django_exceptions.ObjectDoesNotExist as e:
            data = self._process_bad_response("Requested object does not exist.")
            return BadResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            load_serializer = self._process_request_data()
            resource = self.execute(load_serializer)
            if resource is None:
                return NoContentResponse()
            _response_data = self._process_post_response_data(resource)
            return OkResponse(data=_response_data)
        except drf_exceptions.ValidationError as e:
            data = self._process_bad_response(e.__dict__)
            return BadResponse(data)
        except django_exceptions.ValidationError as e:
            data = self._process_bad_response(e.message_dict)
            return BadResponse(data)
        except Exception as e:
            logger.exception(f"{_LOG_PREFIX} {e}")
            data = self._process_bad_response(str(e))
            return BadResponse(data)

    def execute(self, data):
        """
        Every view that inherits this should implement execute() method
        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def fetch_one(self, pk):
        """
        Method for GET requests, every GET view should implement fetch().
        Raises:
            NotImplementedError
        """
        raise NotImplementedError()
