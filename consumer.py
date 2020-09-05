import asyncio
import logging
import websockets


logging.basicConfig(level = logging.INFO)

async def consumer_handler(websocket):
    async for message in websocket:
        log_message(message)

async def consume(url):
    websocket_url = f"{url}"
    async with websockets.connect(websocket_url) as websocket:
        await consumer_handler(websocket)

def log_message(msg):
    logging.info(f"{msg}")


asyncio.get_event_loop().run_until_complete(consume("ws://localhost:8000/ws/polData/"))
asyncio.get_event_loop().run_forever()