from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ScheduleConfig(AppConfig):
    name = "shigoto_q.schedule"
    verbose_name = _("Schedule")

    def ready(self):
        try:
            import shigoto_q.schedule.signals  # noqa F401
        except ImportError:
            pass
