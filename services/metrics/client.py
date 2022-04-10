import statsd
from django.conf import settings


class Telegraf:
    c = None

    def __init__(self, prefix):
        try:
            self.c = statsd.StatsClient(
                settings.STATSD_HOST, settings.STATSD_PORT, prefix=prefix
            )
        except Exception:
            pass

    def incr(self, metric_name):
        self.c.incr(metric_name, 1)


def get_telegraf_client(prefix):
    return Telegraf(prefix)
