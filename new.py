import asyncio
import websockets

async def hello():
    uri = "ws://sim.smogon.com:8000/showdown/websocket"
    async with websockets.connect(uri) as websocket:
        while True:
            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
