from django.conf import settings
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def get_client():
    """
    Function to get the client instead of importing settings everywhere
    """
    return MetricsClient(
        settings.INFLUXDB_URL,
        settings.INFLUXDB_TOKEN,
    )


class MetricsClient:
    """
    InfluxDB client to send metrics to our influx database and
    source it to grafana.
    """

    def __init__(self, url: str, token: str):
        self.token = token
        self.client = InfluxDBClient(
            url=url,
            token=token,
        )
        self.write = self.client.write_api(write_options=SYNCHRONOUS)
        self.query = self.client.query_api()

    def metrics(self, measurement_name: str, value: str, amount: int, tags: dict):
        pass

    def gauge(self, measurement_name: str, value: str, amount: int, tags: dict):
        pass

    def summary(self, measurement_name: str, value: str, amount: int, tags: dict):
        pass

    def post_data(self, measurement_name: str, value: str, amount: int, tags: dict):
        _point = Point(measurement_name).tag(**tags).field(value, amount)
        self.write.write(bucket="shigoto", record=_point)
