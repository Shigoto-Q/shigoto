from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

from shigoto import views as shigoto_views

urlpatterns = [
    path("", shigoto_views.HomePageView.as_view()),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.jwt")),
    path("api/v1/", include("shigoto_q.tasks.urls")),
    path("api/v1/", include("shigoto_q.users.urls")),
    path("api/v1/", include("shigoto_q.github.urls")),
]
urlpatterns += [re_path("^payments/", include("djstripe.urls", namespace="djstripe"))]

# urlpatterns += [re_path(r"^.*$", TemplateView.as_view(template_name="index.html"))]


if settings.DEBUG:

    def trigger_error1(request):
        divison_by_zero = 10 / 0

    urlpatterns += [path("sentry-debug/", trigger_error1)]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
