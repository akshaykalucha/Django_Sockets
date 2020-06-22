# personalchat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import binascii
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['personId']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(self.channel_name)
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        channelList = []
        channelList.append(str(self.channel_name))
        print(channelList)
        print(self.channel_layer, "this is chbannel layer")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        channelName = text_data_json['channel']
        print(channelName, "this is recieved channel name")
        encmsg = bytes(message, 'ascii')
        bin(int(binascii.hexlify(encmsg),16))
        print(encmsg)
        # Send message to room group
        await self.channel_layer.send(
            channelName,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))