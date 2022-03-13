from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djstripe.models import Plan, Product
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from shigoto_q.github.api.serializers import GitHubProfileSerializer
from rest.serializers import CamelCaseSerializer

from ...tasks.api.serializers import (
    ClockedSerializer,
    CrontabSerializer,
    IntervalSerializer,
    SolarSerializer,
    TaskGetSerializer,
)

User = get_user_model()


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["amount", "interval", "trial_period_days", "id"]


class ProductSerializer(CamelCaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    plan_set = serializers.CharField()
    metadata = serializers.CharField()


class UserListSerializer(CamelCaseSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    company = serializers.CharField(required=False)
    country = serializers.CharField(required=False)


class UserLoadSerializer(UserListSerializer):
    password = serializers.CharField(required=True)


class UserDumpSerializer(UserListSerializer):
    pass


class UserSerializerDAB(DjoserUserSerializer):
    crontab = CrontabSerializer(read_only=True, many=True)
    task = TaskGetSerializer(read_only=True, many=True)
    interval = IntervalSerializer(read_only=True, many=True)
    solar = SolarSerializer(read_only=True, many=True)
    clocked = ClockedSerializer(read_only=True, many=True)
    github = GitHubProfileSerializer(read_only=True)

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = [
            "username",
            "github",
            "email",
            "first_name",
            "last_name",
            "country",
            "city",
            "zip_code",
            "state",
            "subscription",
            "customer",
            "crontab",
            "interval",
            "clocked",
            "solar",
            "task",
        ]


class UserCreateSerializer(DjoserUserCreateSerializer):
    password = serializers.CharField(
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "company",
            "password",
            "zip_code",
            "city",
            "country",
        ]


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


class CustomTokenSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    class Meta:
        model = Token
        fields = ["auth_token"]


class SubscriberSerializer(CamelCaseSerializer):
    email = serializers.EmailField()


class UserLogoutSerializer(CamelCaseSerializer):
    refresh_token = serializers.CharField()
