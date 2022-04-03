import logging

from rest.common.types import Page
from rest.responses import OkResponse
from rest.views.base import BaseView

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[REST-RESOURCE-LIST]"


class ResourceListView(BaseView):
    def get(self, request, *args, **kwargs):
        self._process_get_params()
        resource = self.fetch(self.get_data, self.page)
        count = resource.count
        page = resource.page
        data = self._process_post_response_data(resource)
        return OkResponse(dict(count=count, data=data, page=page))

    def _process_post_response_data(self, resource):
        response_data = self.get_dump_serializer(
            data=resource.data,
            many=True,
        )
        response_data.is_valid(raise_exception=True)
        return response_data.data

    def fetch(self, filters: dict, pagination: Page):
        """
        Method for GET requests, every GET view should implement fetch().
        Raises:
            NotImplementedError

        """
        raise NotImplementedError()
