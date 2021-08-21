from __future__ import absolute_import

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shigoto_q.github.api.serializers import (
    GitHubProfileSerializer,
    RepositorySerializer,
)
from shigoto_q.github.models import GitHubProfile


class GitHubList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = GitHubProfile.objects.all()
    serializer_class = GitHubProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request)
        return self.create(request, *args, **kwargs)


class CreateListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        """if an array is passed, set serializer to many"""
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)


class RepositoryList(APIView):
    serializer_class = RepositorySerializer

    def post(self, request, format=None):
        serializer = RepositorySerializer(
            data=request.data,
            many=True,
            context=self.request,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
