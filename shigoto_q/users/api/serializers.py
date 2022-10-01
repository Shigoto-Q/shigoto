from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest.serializers import CamelCaseSerializer

User = get_user_model()


class ProductSerializer(CamelCaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    plan_set = serializers.CharField()
    metadata = serializers.CharField()


class UserListSerializer(CamelCaseSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    company = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)


class UserLoadSerializer(UserListSerializer):
    password = serializers.CharField(required=False)


class UserDumpSerializer(UserListSerializer):
    is_first_login = serializers.BooleanField(required=False)
    two_factor_enabled = serializers.BooleanField(required=False)


class SubscriberSerializer(CamelCaseSerializer):
    email = serializers.EmailField(required=False)


class UserLogoutSerializer(CamelCaseSerializer):
    refresh_token = serializers.CharField()


class OTPSerializer(CamelCaseSerializer):
    url = serializers.CharField(required=False)


class TokenSerializer(serializers.Serializer):
    token = serializers.IntegerField()


class UnSubscriberSerializer(CamelCaseSerializer):
    email = serializers.EmailField(required=False)
