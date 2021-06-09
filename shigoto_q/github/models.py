from django.db import models


class GitHubProfile(models.Model):
    login = models.CharField(max_length=256, default="")
    avatar_url = models.URLField()
    repos_urls = models.URLField()
    public_repos = models.IntegerField()
    public_gists = models.IntegerField()


class Repository(models.Model):
    repo_author = models.ForeignKey(GitHubProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300, default="")
    repo_url = models.URLField()
