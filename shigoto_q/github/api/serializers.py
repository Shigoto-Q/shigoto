from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import GitHubProfile, Repository

User = get_user_model()


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = "__all__"


class GitHubProfileSerializer(serializers.ModelSerializer):
    repository_set = RepositorySerializer(read_only=True, many=True)

    class Meta:
        model = GitHubProfile
        fields = [
            "login",
            "token",
            "avatar_url",
            "login",
            "repos_urls",
            "public_repos",
            "public_gists",
            "repository_set",
        ]

    def create(self, validated_data):
        profile = GitHubProfile.objects.create(**validated_data)
        user = self.context["request"].user
        user.github = profile
        user.save()
        return profile
