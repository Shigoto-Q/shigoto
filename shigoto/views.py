from __future__ import absolute_import

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from shigoto.models import AdminConfig
from shigoto.api.serializers import AdminConfigSerializer


class AdminConfigView(generics.ListCreateAPIView):
    queryset = AdminConfig.objects.all()
    serializer_class = AdminConfigSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AdminConfigSerializer(queryset, many=True)
        return Response(serializer.data)
