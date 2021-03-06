from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djstripe.models import Plan, Product
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from rest.serializers import CamelCaseSerializer
from shigoto_q.github.api.serializers import GitHubProfileSerializer

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
    company = serializers.CharField(required=False)
    country = serializers.CharField(required=False)


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
