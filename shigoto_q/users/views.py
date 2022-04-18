from django.contrib.auth import get_user_model

from rest.views import ResourceView
from shigoto_q.users.api.serializers import UserLogoutSerializer, OTPSerializer
from shigoto_q.users.services import two_factor_auth

User = get_user_model()


class UserLogoutView(ResourceView):
    serializer_dump_class = UserLogoutSerializer
    serializer_load_class = UserLogoutSerializer

    def execute(self, data):
        return


class CreateOTPView(ResourceView):
    serializer_dump_class = OTPSerializer
    serializer_load_class = OTPSerializer
    owner_check = True

    def execute(self, data):
        user = User.objects.get(id=data.get("user_id"))
        url = two_factor_auth.create_device_topt_for_user(user=user)
        return dict(url=url)
