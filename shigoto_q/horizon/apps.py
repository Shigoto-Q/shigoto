from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HorizonConfig(AppConfig):
    name = "shigoto_q.horizon"
    verbose_name = _("Horizon")

    def ready(self):
        try:
            import shigoto_q.horizon.signals  # noqa F401
        except ImportError:
            pass
