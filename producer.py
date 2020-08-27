import json
import requests
import asyncio
import websockets, websocket
import redis
import random, time

# async def producer(url):
#     async with websockets.connect(url) as websocket:
#         for i in range(1000):
#             time.sleep(3)
#             msg  = json.dumps({'value': random.randint(1,100)})
#             await websocket.send(msg)


# asyncio.get_event_loop().run_until_complete(producer("ws://localhost:8000/ws/polData/"))


# import binascii

# arr = bytes("hello world", 'ascii')
# print(arr)
# newarr = bin(int(binascii.hexlify(arr),16))
# for byte in arr:
#     print(byte)

# print(newarr)