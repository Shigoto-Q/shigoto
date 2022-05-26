from .base import *  # noqa
from .base import env


STRIPE_LIVE_SECRET_KEY = env("LIVE_SECRET_KEY", default=None)
STRIPE_TEST_SECRET_KEY = env("TEST_SECRET_KEY", default=None)
STRIPE_LIVE_MODE = env("LIVE_MODE", default=False)
DJSTRIPE_WEBHOOK_SECRET = env("WEBHOOK_SECRET", default=None)
STRIPE_SIGNING_SECRET = env("WEBHOOK_SECRET", default=None)
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="ps4DJ3Yd03UX80YHig5jDOtXWAqORqVpO6jj0pqDMCnc5e9lEKIrXm3MxYsGGLd9",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "django"]
CORS_ALLOW_ALL_ORIGINS = True
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT", default=8025)
NSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

INSTALLED_APPS += ["django_extensions"]  # noqa F405
CELERY_TASK_EAGER_PROPAGATES = True
DOCKER_IMAGE_SERVICE = env(
    "DOCKER_IMAGE_SERVICE", default="http://localhost:5050/docker"
)

PERSONAL_PLAN = "prod_Lkw53cNqzIloTv"
PROFESSIONAL_PLAN = "prod_Lkw5PC0FKzB1m3"
BUSINESS_PLAN = "prod_Lkw5I6W0lbmuyI"


STRIPE_SUCCESS_URL = "http://localhost:3000"
STRIPE_CANCEL_URL = "http://localhost:3000"
