# personalchat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import binascii
from channels.layers import get_channel_layer
import redis
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

r = redis.Redis()

channel_layer = get_channel_layer()

class ChatConsumer(AsyncWebsocketConsumer):
    
    #connecting to channel

    AdminRecordID = None
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['personId']
        self.room_group_name = 'chat_%s' % self.room_name

        # creating a feild value pair and adding to redis hash
        channelInfo = {
            f"channel:{self.room_name}": self.channel_name
        }
        r.hmset("channels", channelInfo)


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()



    async def disconnect(self, close_code):

        # Leave room group
        #deleting that channels feild from redis
        r.hdel("channels", f"channel:{self.room_name}")

        #Check if person is a admin
        try:
            print("searchingfor amdin")
            adminchannel = r.get(f"AdminLog{self.room_name}")
            print(adminchannel, "thisis admin")
            if(adminchannel.decode("utf8") == self.channel_name):
                print("admin is disconnecting")
                print("sending connected user the message that admin is disconnecting delete cookie")
                usertosend = r.hget("channels", f"channel:{self.AdminRecordID}")
                print(usertosend.decode("utf8"), "sending thisuser the disconnected mesage")
                await self.channel_layer.send(
                    usertosend.decode("utf8"),
                    {
                        'type': 'adminDiss_message',
                        'myMsg':{
                            'data': "Admin disconnected",
                            'imp': 'AdminDisconnected delete cookies'
                        }
                    }
                )


        except:
            pass

        #try delete channel pending chat if any from redis
        try:
            r.delete(f"user:{self.room_name}")
        except:
            pass

        #removing channel from group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        # Receive message from WebSocket

        #receiving json data
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        try:

            #if message is received by admin
            if text_data_json['type'] == 'byAdmin':
                r.set(f"AdminLog{self.room_name}", self.channel_name)
                #getting users channel id from json
                channelId = text_data_json['channelId']
                if self.AdminRecordID == None:
                    self.AdminRecordID = channelId
                    print(self.AdminRecordID, "setting globaluserid")


                #getting channel value of users ID
                usertosend = r.hget("channels", f"channel:{channelId}")


                #getting all channels in redis hash
                allChannels = r.hgetall('channels')
                for key, value in allChannels.items():
                    if value.decode("utf8") == self.channel_name:
                        myChannelName = key.decode("utf8")


                try:
                    if text_data_json['message'] == 'sendPrevMessages':
                        usermssgs = r.lrange(f"user:{channelId}", 0, -1)
                        pendingMsgList = []
                        for message in usermssgs:
                            pendingMsgList.append((message).decode("utf8"))
                            r.lpop(f"user:{channelId}")
                        if len(pendingMsgList) >= 1:
                            print('there are pending messages')
                            await self.channel_layer.send(
                                self.channel_name,
                                {
                                    'type': 'chat_message',
                                    'message': pendingMsgList
                                })

                            await self.channel_layer.send(
                                usertosend.decode("utf8"),
                                {
                                    'type': 'chat_message',
                                    'message': {
                                        "adminMessage": "Admin connected",
                                        "from": myChannelName
                                    }
                                })


                            return
                        elif len(pendingMsgList) <= 0:
                            print("No user Messages")
                        #print(pendingMsgList)
                        return
                except:
                    pass

                
                #sending this dic to user containing my chnnl id for user to refer which admin it received message from
                messagetosend = {
                    "message": message,
                    "from": myChannelName
                }


                #sending message to users channel and myself
                await self.channel_layer.send(
                    usertosend.decode("utf8"),
                    {
                        'type': 'chat_message',
                        'message': {
                            "adminMessage": message,
                            "from": myChannelName
                        }
                    })
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    })
                return


            #if message is received from user
            if text_data_json['type'] == 'byUser':
                userId = self.room_name
                try:

                    #getting admins channel value from channelId received in json
                    usertosend = r.hget("channels", text_data_json['sendToAdmin'])
                except:
                    usertosend = None
                if text_data_json['sendToAdmin'] == None:
                    print(message, "for admin null")
                    r.rpush(f"user:{userId}", f"{message}")
                    print("No admin connected to this user")
                    await self.channel_layer.send(
                        self.channel_name,
                        {
                            'type': 'adminDiss_message',
                            'myMsg':{
                                'data': message,
                                'imp': 'AdminDisconnected delete cookies'
                            }
                        }
                    )
                    return
                #sending message to myself and admin
                print(usertosend, "message will be sent to this user")
                await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'adminDiss_message',
                    'myMsg':{
                        'data': message,
                    }
                })
                await self.channel_layer.send(
                usertosend.decode("utf8"),
                {
                    'type': 'chat_message',
                    "message": message,
                })
        except:
            pass


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


    async def adminDiss_message(self, event):
        message = event['myMsg']
        await self.send(text_data=json.dumps({
            'myMsg': message
        }))