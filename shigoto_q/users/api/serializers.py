from django.contrib.auth import get_user_model
from rest_framework import serializers
from djstripe.models import Product, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["amount", "interval", "trial_period_days"]


class ProductSerializer(serializers.ModelSerializer):
    plan_set = PlanSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ["name", "plan_set", "metadata"]


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
