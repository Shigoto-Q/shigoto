from django.urls import path, re_path

from .consumers import ResultConsumer, TaskResultConsumer

websocket_urlpatterns = [
    re_path(r"ws/task/", TaskResultConsumer.as_asgi()),
    path("ws/result/", ResultConsumer.as_asgi(), name="ws_result"),
]
