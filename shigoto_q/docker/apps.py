from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DockerConfig(AppConfig):
    name = "shigoto_q.docker"
    verbose_name = _("Docker")

    def ready(self):
        try:
            import shigoto_q.docker.signals  # noqa F401
        except ImportError:
            pass
