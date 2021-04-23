from djstripe.models import Product, Plan
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...tasks.api.serializers import CrontabSerializer


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

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "subscription",
            "customer",
            "total_tasks",
            "crontab",
        ]
        depth = 1


class UserCreateSerializer(DjoserUserCreateSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "company",
            "password",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserCreateSerializer, self).create(validated_data)
