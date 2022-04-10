import json

from rest_framework import serializers


class JSONField(serializers.DictField):
    def to_representation(self, value):
        json_data = {}
        try:
            json_data = json.loads(value)
        except ValueError as e:
            raise e
        return json_data

    def to_internal_value(self, data):
        return json.dumps(data)


class TimezoneField(serializers.Field):
    """
    Serializing TimeZoneFild
    """

    def to_representation(self, obj):
        return obj.zone

    def to_internal_value(self, data):
        return data
