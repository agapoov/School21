import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatGroup, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_uuid = self.scope['url_route']['kwargs']['group_uuid']
        self.room_group_name = f'chat_{self.group_uuid}'

        session = self.scope["session"]
        user_id = session.get('user_id')

        if user_id:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if not self.scope["session"].get('user_id'):
            return

        group = await database_sync_to_async(ChatGroup.objects.get)(uuid=self.group_uuid)
        user = self.scope["user"]

        message_obj = await self.save_message(group, user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
                'timestamp': message_obj.timestamp.strftime('%H:%M'),
                'user_id': self.scope["session"].get('user_id'),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        user_id = event['user_id']
        timestamp = event['timestamp']

        is_user_message = str(user_id) == str(self.scope["session"].get('user_id'))

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'user_id': user_id,
            'timestamp': timestamp,
            'is_user_message': is_user_message,
        }))

    @database_sync_to_async
    def save_message(self, group, user, message_content):
        return ChatMessage.objects.create(
            group=group,
            user=user,
            message=message_content,
        )
