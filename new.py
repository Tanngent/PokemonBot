import asyncio
import websockets
import requests

async def hello():
	uri = "ws://sim.smogon.com:8000/showdown/websocket"
	async with websockets.connect(uri) as websocket:
		greeting = await websocket.recv();
		print(f"< {greeting}")
		while True:
			greeting = await websocket.recv()
			print(f"< {greeting}")
			url = "https://play.pokemonshowdown.com/~~showdown/action.php"

asyncio.get_event_loop().run_until_complete(hello())
