from .base import *  # noqa
from .base import env

STRIPE_LIVE_SECRET_KEY = "pk_test_518h2jFItAhzYJ7dgwgnoYIDrufudKMsxdhAaa2YZt0YcbM5z1EfBvxYprkufs4KJO76zTkfaXSS3OSBtn6GMDmMm00C1wwlqJb"
STRIPE_TEST_SECRET_KEY = "sk_test_518h2jFItAhzYJ7dgGweqmPd6Nvt8f9i2JxMdSxJZlh9j2fARaWnW03AQC9VsqCUhJB5iSxH3a7OS2KF1L29Y4gVO00DVPtLlf6"
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_8v7igqtCb4yNSNqQHsLD9KJiq7k4TK7F"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
STRIPE_SIGNING_SECRET = "whsec_8v7igqtCb4yNSNqQHsLD9KJiq7k4TK7F"
DJSTRIPE_USE_NATIVE_JSONFIELD = (
    True  # We recommend setting to True for new installations
)
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"  # Set to `"id"` for all new 2.4+ installations

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="ps4DJ3Yd03UX80YHig5jDOtXWAqORqVpO6jj0pqDMCnc5e9lEKIrXm3MxYsGGLd9",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
CORS_ALLOW_ALL_ORIGINS = True
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = 1025
NSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

INSTALLED_APPS += ["django_extensions"]  # noqa F405
CELERY_TASK_EAGER_PROPAGATES = True
