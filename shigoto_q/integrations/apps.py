from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IntegrationsConfig(AppConfig):
    name = "shigoto_q.integrations"
    verbose_name = _("Integrations")

    def ready(self):
        try:
            import shigoto_q.integrations.signals  # noqa F401
        except ImportError:
            pass
