import asyncio
import websockets
import requests
import json

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
		header = {'Content-type': 'application/x-www-form-urlencoded; encoding=UTF-8'}
		content = {'act': 'login', 'name': '0hzlf9CCSL','pass': '123456', 'challstr': greeting[10:]}
		print(content)
		r = requests.post(url,data=content,headers=header)
		print(r.text[1:])
		s = json.loads(r.text[1:])
		print(s)
		l = "|/trn 0hzlf9CCSL,0," + s['assertion']
		print(l)
		await websocket.send(l)
		while True:
			greeting = await websocket.recv();
			print(f"< {greeting}")
		

asyncio.get_event_loop().run_until_complete(hello())
