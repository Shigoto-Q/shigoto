from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import JsonResponse
from django.urls import include, path, re_path


urlpatterns = [
    re_path("^payments/", include("djstripe.urls", namespace="djstripe")),
    path("api/", include("shigoto_q.urls")),
    path("public/", include("docs.urls")),
]
