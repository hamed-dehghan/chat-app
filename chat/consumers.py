# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Chat, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"chat_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']

        # Store the message in the database
        receiver = await User.objects.get(id=receiver_id)
        Chat.objects.create(sender=self.scope['user'], receiver=receiver, message=message)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
        }))
