import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer

from .api.serializers import TaskResultSerializer
from .models import TaskResult


class ResultConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self, *args, **kwargs):
        await self.accept()
        await self.channel_layer.group_add(
            "result",
            self.channel_name,
        )

    async def webocket_notify(self, event):
        print(event)
        await self.send_json(event["content"])

    async def receive_json(self, content, **kwargs):
        group_name = "result"
        self.groups.append(group_name)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name,
        )

    async def get_serializer(self, *, data):
        pass


async def update_result(data):
    serializer = TaskResultSerializer(data)
    channel_layer = get_channel_layer()
    content = {
        "type": "UPDATE_RESULT",
        "payload": serializer.data,
    }

    await channel_layer.group_send(
        "result",
        {
            "type": "websocket.notify",
            "content": content,
        },
    )


class TaskResultConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        self.is_connected = True

    async def websocket_receive(self, event):
        tasks = await self.get_user_tasks()
        await self.send({"type": "websocket.send", "text": json.dumps(tasks)})
        while self.is_connected:
            await asyncio.sleep(1)
            tasks = await self.get_user_tasks()
            await self.send({"type": "websocket.send", "text": json.dumps(tasks)})

    async def websocket_disconnect(self, event):
        self.is_connected = False
        await self.send({"type": "websocket.disconnect"})

    @database_sync_to_async
    def get_user_tasks(self):
        tasks = TaskResult.objects.filter(user=self.scope.get("user"))
        serializer = TaskResultSerializer(tasks, many=True)
        return serializer.data
