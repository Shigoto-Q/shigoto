from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = "shigoto_q.products"
    verbose_name = _("products")

    def ready(self):
        try:
            import shigoto_q.products.signals  # noqa F401
        except ImportError:
            pass
