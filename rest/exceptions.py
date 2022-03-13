from django.core import exceptions as django_exceptions
from rest_framework import exceptions as drf_exceptions


class BaseRestError(Exception):
    pass


class RestValidationError:
    pass
