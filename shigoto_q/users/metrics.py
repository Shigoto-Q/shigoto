from services.metrics.client import get_telegraf_client

metrics = get_telegraf_client("users")
