import logging
from datetime import timedelta
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "shigoto_q"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)

if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR / ".env"))

DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

DJANGO_APPS = [
    "channels",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "corsheaders",
    "django_celery_results",
    "djstripe",
    "django_elasticsearch_dsl",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "mjml",
    "post_office",
]

ELASTICSEARCH_DSL = {
    "default": {"hosts": "localhost:9200"},
}

LOCAL_APPS = [
    "shigoto_q.users.apps.UsersConfig",
    "shigoto_q.tasks.apps.TasksConfig",
    "shigoto_q.github.apps.GithubConfig",
    "shigoto_q.schedule.apps.ScheduleConfig",
    "shigoto_q.kubernetes.apps.KubernetesConfig",
    "shigoto_q.docker.apps.DockerConfig",
    "shigoto_q.emails.apps.EmailsConfig",
    "shigoto_q.integrations.apps.IntegrationsConfig",
    "shigoto_q.products.apps.ProductsConfig",
    "shigoto_q.features.apps.FeatureConfig",
    "shigoto_q.horizon.apps.HorizonConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
MIGRATION_MODULES = {"sites": "shigoto_q.contrib.sites.migrations"}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_URL = "shigoto_q.users.token_obtain_pair"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [str(APPS_DIR / "static")]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "emails/templates/")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "post_office.template.backends.post_office.PostOfficeTemplates",
        "DIRS": [str(APPS_DIR / "emails/templates/")],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
            ]
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"


FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_TIMEOUT = 5
ADMIN_URL = "admin/"
ADMINS = [("""Simeon Aleksov""", "simeon.aleksov@shigo.to")]
MANAGERS = ADMINS


# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "simple": {
#             "format": "[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "INFO",
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#         "logstash": {
#             "level": "DEBUG",
#             "class": "logstash.TCPLogstashHandler",
#             "host": "logstash",
#             "port": 5000,
#             "version": 1,
#             "message_type": "django",
#             "fqdn": True,
#             "tags": ["django.request"],
#         },
#     },
#     "loggers": {
#         "django.request": {
#             "handlers": ["logstash"],
#             "level": "INFO",
#             "propagate": True,
#         },
#         "django": {
#             "handlers": ["logstash"],
#             "level": "INFO",
#             "propagate": True,
#             "stream": "ext://sys.stdout",
#         },
#         "shigoto_q.tasks.services.tasks": {
#             "handlers": ["console", "logstash"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#         "shigoto_q": {
#             "handlers": ["console", "logstash"],
#             "level": "DEBUG",
#             "propagate": True,
#             "stream": "ext://sys.stdout",
#         },
#     },
# }

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DATETIME_FORMAT": "%Y-%m-%d - %H:%M:%S",
    "LAST_LOGIN": True,
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN": True,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://shigo.to",
    "https://shigo.to",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,
    event_level=logging.ERROR,
)
integrations = [
    sentry_logging,
    DjangoIntegration(),
    CeleryIntegration(),
    RedisIntegration(),
]
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="local"),
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.25),
)

INFLUXDB_HOST = env("INFLUXDB_HOST")
INFLUXDB_PORT = env("INFLUXDB_PORT")

INFLUXDB_TOKEN = env("INFLUXDB_TOKEN")
INFLUXDB_URL = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}"


REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")

DIND_HOST = env("DIND_HOST")
DIND_PORT = env("DIND_PORT", default=2375)

DOCKER_IMAGE_PREFIX = env("DOCKER_IMAGE_PREFIX", default="shigoto")

UPDATE_LAST_LOGIN = True

TEMP_REPOSITORY_DIR = "tmp/{user_id}/repositories/"
DOCKER_TAG_PREFIX = "shigoto/"

MJML_EXEC_CMD = "./node_modules/mjml/bin/mjml"
MJML_CHECK_CMD_ON_STARTUP = False

DEFAULT_INFO_EMAIL = "info@shigo.to"
DEFAULT_SUPPORT_EMAIL = "support@shigo.to"

POST_OFFICE = {
    "LOG_LEVEL": 2,
    "SENDING_ORDER": ["created"],
    "CELERY_ENABLED": True,
}

STATSD_HOST = env("TELEGRAF_HOST")
STATSD_PORT = env("TELEGRAF_PORT")
STATSD_PREFIX = None
STATSD_MAXUDPSIZE = 512
STATSD_IPV6 = False

STRIPE_API_KEY = ""

FIELD_ENCRYPTION_KEY = "7ySVjUlysoLjXTs24yIbrYArwGENoD9r_GHl-xMfu-w="
