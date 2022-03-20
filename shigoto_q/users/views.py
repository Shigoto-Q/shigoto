import json

import djstripe
import stripe
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djstripe.settings import STRIPE_SECRET_KEY

from rest.views import ResourceView
from shigoto_q.users.services import subscribers
from shigoto_q.users.api.serializers import SubscriberSerializer, UserLogoutSerializer

stripe.api_key = STRIPE_SECRET_KEY


class UserLogoutView(ResourceView):
    serializer_dump_class = UserLogoutSerializer
    serializer_load_class = UserLogoutSerializer

    def execute(self, data):
        return subscribers.blacklist_token(data)


class SubscriberCreateView(ResourceView):
    serializer_dump_class = SubscriberSerializer
    serializer_load_class = SubscriberSerializer
    permission_classes = []
    owner_check = False

    def execute(self, data):
        return subscribers.create_subscriber(data)
