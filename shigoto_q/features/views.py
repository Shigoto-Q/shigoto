from rest.common.fetch import fetch_and_paginate
from rest.common.types import Page
from rest.views import ResourceListView
from shigoto_q.features.api import serializers
from shigoto_q.features.api import messages
from shigoto_q.features import services


class URLListView(ResourceListView):
    serializer_dump_class = serializers.URLListSerializer
    serializer_load_class = serializers.URLListSerializer
    feature_flag = 'ff01_features'

    def fetch(self, filters, pagination):

        return fetch_and_paginate(
            func=services.get_urls,
            filters=filters,
            pagination=Page(size=0, page=1),
            serializer_func=messages.URL.from_dict,
        )
