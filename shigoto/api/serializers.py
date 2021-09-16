from __future__ import absolute_import

from rest_framework import serializers

from shigoto.models import AdminConfig


class AdminConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminConfig
        fields = ["environment", "repository", "notes", "base_url"]
