from django.contrib.auth import get_user_model
from rest_framework import generics, mixins

from .api.serializers import GitHubProfileSerializer, RepositorySerializer
from .models import GitHubProfile, Repository


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


class RepositoryList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
