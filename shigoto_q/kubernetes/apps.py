from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KubernetesConfig(AppConfig):
    name = "shigoto_q.kubernetes"
    verbose_name = _("Kubernetes")

    def ready(self):
        try:
            import shigoto_q.kubernetes.signals  # noqa F401
        except ImportError:
            pass
