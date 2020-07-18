# graphsocket/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer



class DataConsumer(AsyncWebsocketConsumer):
    

    async def connect(self):
        self.groupname = 'dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code): #close code is just like status code
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
    
    async def receive(self, text_data): #this will recieve all the data from websocket
        data = json.loads(text_data)
        val = data['value']

        await self.channel_layer.group_send(
            self.groupname,
            {
                'type': 'deprocessing',
                'value': val
            }
        )
        print(">>>", text_data)

    async def deprocessing(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({'value': valOther}))



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(self.channel_name, "this is channel name")
        print("this is thr graphchannel")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
