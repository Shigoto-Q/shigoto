from django.db import models


class GitHubProfile(models.Model):
    login = models.CharField(max_length=256, default="")
    avatar_url = models.URLField()
    repos_urls = models.URLField()
    public_repos = models.IntegerField()
    public_gists = models.IntegerField()
    token = models.CharField(max_length=128, default="")


class Repository(models.Model):
    repo_author = models.ForeignKey(GitHubProfile, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=300, default="")
    repo_url = models.URLField()
    language = models.CharField(max_length=120, default="", null=True)
