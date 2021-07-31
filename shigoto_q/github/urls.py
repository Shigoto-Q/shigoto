from __future__ import absolute_import

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from shigoto_q.github.views import GitHubList, RepositoryList

urlpatterns = [
    path("github/profile/", GitHubList.as_view()),
    path("github/repository/", RepositoryList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
