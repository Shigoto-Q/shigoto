from __future__ import absolute_import

from django.contrib import admin

from shigoto_q.github.models import GitHubProfile, Repository


@admin.register(GitHubProfile)
class GitHubProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "login",
        "avatar_url",
        "repos_urls",
        "public_repos",
        "public_gists",
        "token",
    )


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("id", "repo_author", "full_name", "repo_url")
    list_filter = ("repo_author",)
