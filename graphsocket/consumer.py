# graphsocket/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

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