from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djstripe.models import Plan, Product
from rest_framework import serializers

from ...tasks.api.serializers import CrontabSerializer, TaskGetSerializer

User = get_user_model()


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["amount", "interval", "trial_period_days", "id"]


class ProductSerializer(serializers.ModelSerializer):
    plan_set = PlanSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        ordering = [
            "plan_set",
        ]
        fields = ["id", "name", "plan_set", "metadata"]


class UserSerializer(DjoserUserSerializer):
    crontab = CrontabSerializer(read_only=True, many=True)
    task = TaskGetSerializer(read_only=True, many=True)

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = [
            "username",
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
