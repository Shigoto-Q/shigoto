import logging

import redis
from django.conf import settings

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[REDIS-CLIENT]"


def get_client():
    return RedisClient


class RedisClient:
    client = redis.StrictRedis(
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        charset="utf-8",
        decode_responses=True,
    )

    @classmethod
    def publish(cls, channel: str, data: str) -> None:
        cls.client.publish(channel, data)
        logger.info(f"{_LOG_PREFIX} Published to channel {channel}, data: {data}")
        print(f"{_LOG_PREFIX} Published to channel {channel}, data: {data}")
