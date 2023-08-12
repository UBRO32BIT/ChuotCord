import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MessageGroup, Group, GroupUser

class ChatConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def get_group(self):
        return Group.objects.get(id=self.room_name)
    
    @database_sync_to_async
    def save_message(self, message):
        return message.save()
    
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created_at = event['created_at']
        await self.send_json({
            'type': 'chat',
            'user': username,
            'message': message,
            'created_at': created_at
        })

    async def receive(self, text_data):
        response = json.loads(text_data)
        message = response['message']

        group = await self.get_group()
        if (True):
            message_object = MessageGroup(member=self.user, group=group, content=message)
            await self.save_message(message_object)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'username': self.user.username,
                    'created_at': message_object.created_at.strftime('%d-%m-%Y, %H:%M:%S'),
                    'message':message
                }
            )
        print("Message: ", message)

