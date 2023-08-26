import json
from collections import defaultdict
import base64
import pytz
from datetime import datetime
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MessageGroup, Group

class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_connected_users = defaultdict(set)
    @database_sync_to_async
    def get_group(self):
        return Group.objects.get(id=self.room_name)
    
    @database_sync_to_async
    def save_message(self, message):
        return message.save()
    
    @database_sync_to_async
    def get_latest_message(self):
        return MessageGroup.objects.latest('id')
    
    @database_sync_to_async
    def save_image(self, message_object, image_filename, image_content):
        return message_object.image.save(image_filename, image_content)
    
    async def user_connect(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'player_connect',
            'message': message
        }))

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

        self.room_connected_users[self.room_name].add(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_connect',
                'message': [user.username for user in self.room_connected_users[self.room_name]] #list(self.room_connected_users[self.room_name])
            }
        )

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
        )
        self.room_connected_users[self.room_name].remove(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_connect',
                'message': [user.username for user in self.room_connected_users[self.room_name]] #list(self.room_connected_users[self.room_name])
            }
        )
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created_at = event['created_at']
        image = event['image']
        await self.send_json({
            'type': 'chat',
            'user': username,
            'message': message,
            'created_at': created_at,
            'image': image
        })

    async def receive(self, text_data):
        # Load json requests from client-side
        response = json.loads(text_data)
        # Fetch data from request
        message_type = response['type']
        message = response['message']
        # Get group chat from the consumer object
        group = await self.get_group()
        # IMPLEMENT SECURITY LAYER LATER
        if (True):
            # Create message object
            message_object = MessageGroup(member=self.user, group=group, content=message)
            image = None
            # Check if the request type is chat with images
            if (message_type == 'chat_with_image'):
                # Decode base64 string to byte
                base64_image = response['image']
                image_data = base64.b64decode(base64_image.split(',')[1])

                # Get the latest message ID from the database
                latest_message = await self.get_latest_message()

                # Use the message ID as the image filename
                image_filename = f'{latest_message.id}_received_image.png'
                image_content = ContentFile(image_data, name=image_filename)
                
                await self.save_image(message_object, image_filename, image_content)
                
                # Construct the image URL
                image = message_object.image.url

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
                        'image': image,
                        'message':message
                    }
                )
        print("Message: ", message, " ", message_object.created_at, " ")

