from django.urls import path, re_path
from .consumers import TaskResultConsumer

websocket_urlpatterns = [
    re_path(r"ws/task/results/", TaskResultConsumer.as_asgi()),
]
