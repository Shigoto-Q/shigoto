import stripe
from djstripe.settings import STRIPE_SECRET_KEY
from rest_framework.permissions import AllowAny

from rest.views import ResourceView
from shigoto_q.users.api.serializers import SubscriberSerializer, UserLogoutSerializer
from shigoto_q.users.services import subscribers

stripe.api_key = STRIPE_SECRET_KEY


class UserLogoutView(ResourceView):
    serializer_dump_class = UserLogoutSerializer
    serializer_load_class = UserLogoutSerializer

    def execute(self, data):
        return subscribers.blacklist_token(data)
