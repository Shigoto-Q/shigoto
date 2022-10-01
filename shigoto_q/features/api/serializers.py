from rest.serializers import CamelCaseSerializer

from rest_framework import serializers


class URLListSerializer(CamelCaseSerializer):
    url = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
