from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status

from shigoto_q.users.api.serializers import TokenSerializer


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def create_device_topt_for_user(user):
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=False)
    return device.config_url


def validate_user_otp(user, data):
    device = get_user_totp_device(user)
    serializer = TokenSerializer(data=data)

    if not serializer.is_valid():
        return dict(data="Invalid data", status=status.HTTP_400_BAD_REQUEST)
    elif device is None:
        return dict(data="No device registered.", status=status.HTTP_400_BAD_REQUEST)
    elif device.verify_token(serializer.data.get("token")):
        if not device.confirmed:
            device.confirmed = True
            device.save()
            return dict(
                data="Successfully confirmed and saved device..",
                status=status.HTTP_201_CREATED,
            )
        else:
            return dict(data="OTP code has been verified.", status=status.HTTP_200_OK)
    else:
        return dict(
            data=dict(
                statusText="The code you entered is invalid",
                status=status.HTTP_400_BAD_REQUEST,
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )
