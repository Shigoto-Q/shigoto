from rest_framework import serializers

from rest.serializers import CamelCaseSerializer


class CustomerSubscriptionSerializer(CamelCaseSerializer):
    email = serializers.EmailField(required=False)
    plan_id = serializers.CharField(required=False)


class SessionSerializer(CamelCaseSerializer):
    price_id = serializers.CharField(required=False)


class SessionDumpSerializer(CamelCaseSerializer):
    session_id = serializers.CharField(required=False)
