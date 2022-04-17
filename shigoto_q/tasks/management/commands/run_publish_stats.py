from __future__ import absolute_import

import time
import json
import logging

from django.core.management.base import BaseCommand

from services.redis.client import get_client
from shigoto_q.docker.services.docker import get_total_docker_images
from shigoto_q.tasks.services.tasks import get_total_task_results
from shigoto_q.kubernetes.services.kubernetes import get_total_deployments

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[PUBLISH-STATS-COMMAND]"
redis_client = get_client()


class Command(BaseCommand):
    help = "Long running command to publish stats to redis."
    _SLEEP_TIME = 1.5
    _CHANNEL = "shigoto-stats"

    @classmethod
    def publish_stats(cls):
        while True:
            try:
                total_task_results = get_total_task_results()
                total_kubernetes_deployments = get_total_deployments()
                total_docker_images = get_total_docker_images()
                data = dict(
                    totalTaskResults=total_task_results,
                    totalKubernetesDeployments=total_kubernetes_deployments,
                    totalDockerImages=total_docker_images,
                )
                redis_client.publish(cls._CHANNEL, json.dumps(data))
                time.sleep(cls._SLEEP_TIME)
            except Exception:
                logger.exception(
                    f"{_LOG_PREFIX} Caught an exception while publishing stats."
                )
                break

    def handle(self, *args, **options):
        self.stdout.write("Starting statistics number publish.")
        self.publish_stats()
