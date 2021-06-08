import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .api.serializers import TaskResultSerializer
from .models import TaskResult


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
