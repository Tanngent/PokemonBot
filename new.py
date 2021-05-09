import asyncio
import websockets
import requests

async def hello():
	uri = "ws://sim.smogon.com:8000/showdown/websocket"
	url = "https://play.pokemonshowdown.com/~~showdown/action.php"
	async with websockets.connect(uri) as websocket:
		greeting = await websocket.recv();
		print(f"< {greeting}")
		greeting = await websocket.recv();
		print(f"< {greeting}")
		greeting = await websocket.recv();
		print(f"< {greeting}")
		greeting = await websocket.recv();
		print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
