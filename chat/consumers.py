import json
import pytz
from datetime import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MessageGroup, Group

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
            # Get the UTC time zone
            utc_timezone = pytz.timezone('UTC')
            
            # Convert the created_at timestamp to UTC
            created_at_utc = message_object.created_at.astimezone(utc_timezone)
            
            # Convert the UTC timestamp to the desired time zone
            desired_timezone = pytz.timezone('Asia/Bangkok')  # Replace with your desired time zone
            created_at_desired_timezone = created_at_utc.astimezone(desired_timezone)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'username': self.user.username,
                    'created_at': created_at_desired_timezone.strftime('%d-%m-%Y, %H:%M:%S'),
                    'message':message
                }
            )
        print("Message: ", message, " ", message_object.created_at)

