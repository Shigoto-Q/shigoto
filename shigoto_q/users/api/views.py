from __future__ import absolute_import

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from rest.common.fetch import fetch_and_paginate
from rest.views import ResourceListView, ResourceView
from shigoto_q.users.api.serializers import (
    UserDumpSerializer,
    UserListSerializer,
    UserLoadSerializer,
    SubscriberSerializer,
    UnSubscriberSerializer,
)
from shigoto_q.users.services import users as user_services
from shigoto_q.users.services import subscribers as subscriber_services
from shigoto_q.users.api import messages as user_messages

User = get_user_model()


class UsersListView(ResourceListView):
    serializer_dump_class = UserListSerializer
    serializer_load_class = UserListSerializer

    def fetch(self, filters, pagination):
        return fetch_and_paginate(
            func=user_services.list_users,
            filters=filters,
            pagination=pagination,
            serializer_func=user_messages.User.from_model,
            is_serializer_dataclass=True,
        )


class UserView(ResourceView):
    serializer_dump_class = UserDumpSerializer
    serializer_load_class = UserLoadSerializer
    request_param = "user"
    owner_check = True

    def fetch_one(self, pk):
        if pk == "me":
            pk = self.request.user.id
        return user_services.get_user(pk=pk)


class UserCreateView(ResourceView):
    serializer_dump_class = UserDumpSerializer
    serializer_load_class = UserLoadSerializer
    http_method_names = ["post"]
    permission_classes = []

    def execute(self, data):
        return user_services.create_user(data=data)


class SubscriberView(ResourceView):
    serializer_dump_class = SubscriberSerializer
    serializer_load_class = SubscriberSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def execute(self, data):
        return subscriber_services.create_subscriber(data)


class UnsubscribeView(ResourceView):
    serializer_dump_class = UnSubscriberSerializer
    serializer_load_class = UnSubscriberSerializer
    permission_classes = [AllowAny]

    def execute(self, data):
        return subscriber_services.remove_subscriber(email=data.get("email"))
