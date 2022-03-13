from collections import OrderedDict

from rest_framework import serializers
from rest_framework import status

from rest.utils import CaseConverter


class CamelCaseSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        for field_name, field in list(data.items()):
            data[CaseConverter.camel_case_to_snake_case(field_name)] = data.pop(
                field_name
            )
        return super(CamelCaseSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        ret = super(CamelCaseSerializer, self).to_representation(instance)
        for field_name, field in list(ret.items()):
            ret[CaseConverter.snake_case_to_camel_case(field_name)] = ret.pop(
                field_name
            )
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])


class BadResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=status.HTTP_400_BAD_REQUEST)
    message = serializers.DictField(required=True)


class ResourceListResponseSerializer(CamelCaseSerializer):
    data = serializers.ListField(
        child=serializers.DictField(),
    )
    count = serializers.IntegerField()
