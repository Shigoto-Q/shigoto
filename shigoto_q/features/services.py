import json
import logging

from django.db import transaction
from django.core.cache import cache
from django.core.management import call_command
from django_extensions.management.commands import show_urls

from shigoto_q.features.models import FeatureFlag
from shigoto_q.features.definitions import FEATURE_FLAGS
from shigoto_q.features.constants import (
    FEATURE_FLAG_CACHE_KEY,
    FEATURE_FLAG_TTL,
    URLS_CACHE_KEY,
    URLS_CACHE_TTL,
)


_LOG_PREFIX = "[FEATURE-FLAG-SERVICE]"
logger = logging.getLogger(__name__)


class FeatureFlagService:
    @classmethod
    def create_feature_flag(
        cls,
        definition: str,
        description: str,
        enabled: bool,
        users: list = None,
    ):
        obj, _ = FeatureFlag.objects.get_or_create(
            description=description,
            definition=definition,
            enabled=enabled,
        )
        if users:
            obj.users.add(*users)
        logger.info(
            f"{_LOG_PREFIX} Creating feature flag with definition: {definition}."
        )
        cls._invalidate_cache()
        return obj

    @classmethod
    def create_feature_flags_from_definitions(cls):
        logger.info(f"{_LOG_PREFIX} Creating all feature flags from definitions.")
        for feature_flag in FEATURE_FLAGS:
            cls.create_feature_flag(
                **feature_flag,
            )

    @classmethod
    def is_flag_enabled(cls, definition: str):
        flag = FeatureFlag.objects.filter(definition=definition).first()
        return flag.enabled

    @classmethod
    def toggle_flag(cls, definition: str, enabled: bool):
        status = "enabled" if enabled else "disabled"
        logger.info(f"{_LOG_PREFIX} Setting feature flag {definition} to {status}.")
        with transaction.atomic():
            flag = (
                FeatureFlag.objects.filter(definition=definition)
                .select_for_update()
                .first()
            )
            flag.enabled = enabled
            flag.save(update_fields=["enabled"])
            cls._invalidate_cache()

    @classmethod
    def get_flag_by_definition(cls, **kwargs):
        flags = FeatureFlag.objects.filter(**kwargs).values()
        return flags

    @classmethod
    def get_all_defined_flags(cls):
        cached_flags = cls._get_cached_flags()
        if cached_flags:
            return cached_flags

        definitions = cls._get_local_definitions()
        flags = cls.get_flag_by_definition(
            definition__in=definitions,
        )
        cls._cache_feature_flags(flags=list(flags))
        return list(flags)

    @classmethod
    def _cache_feature_flags(cls, flags: list):
        cache.set(FEATURE_FLAG_CACHE_KEY, flags, FEATURE_FLAG_TTL)

    @classmethod
    def _get_cached_flags(cls):
        return cache.get(FEATURE_FLAG_CACHE_KEY)

    @classmethod
    def _invalidate_cache(cls):
        cache.delete(FEATURE_FLAG_CACHE_KEY)

    @classmethod
    def is_flag_defined(cls, definition):
        definitions = cls._get_local_definitions()
        return definition in definitions

    @classmethod
    def _get_local_definitions(cls):
        return [flag["definition"] for flag in FEATURE_FLAGS]


def get_urls():
    cached_urls = cache.get(URLS_CACHE_KEY)
    if cached_urls is not None:
        return json.loads(cached_urls)
    urls = call_command(show_urls.Command(), format="json")
    cache.set(URLS_CACHE_KEY, urls, URLS_CACHE_TTL)
    return json.loads(urls)
