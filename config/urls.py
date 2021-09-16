from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [
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
    path("backoffice/api/", include("shigoto.urls"))
]
urlpatterns += [re_path("^payments/", include("djstripe.urls", namespace="djstripe"))]


react_urls = [re_path(r"^.*$", TemplateView.as_view(template_name="index.html"))]


if settings.DEBUG:
    react_urls = []
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

urlpatterns += react_urls
