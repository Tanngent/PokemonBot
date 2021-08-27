import asyncio
import websockets
import requests
import json

async def inp(queue, websocket):
	url = "https://play.pokemonshowdown.com/~~showdown/action.php"
	greeting = await websocket.recv()
	print(f"<<< {greeting}")
	while not greeting.startswith("|challstr|"):
		greeting = await websocket.recv()
		print(f"<<< {greeting}")
	f = open("user.txt","r")
	usname = f.readline()
	passwd = f.readline()
	header = {'Content-type': 'application/x-www-form-urlencoded; encoding=UTF-8'}
	content = {'act': 'login', 'name': usname[:-1],'pass': passwd, 'challstr': greeting[10:]}
	r = requests.post(url,data=content,headers=header)
	s = json.loads(r.text[1:])
	l = "|/trn " + usname[0:-1] +",0," + s['assertion']
	await queue.put(l)
	while True:
		greeting = await websocket.recv()
		print(f"<<< {greeting}")
		if greeting.startswith("|updatesearch|"):
			s = json.loads(greeting[14:])
			if s['games']:
				asyncio.gather(asyncio.create_task(battle(asyncio.Queue(),queue,list(s['games'].keys())[0])))
		elif greeting.startswith("|pm|"):
			bits = greeting.split("|")
			other = bits[2].strip()
			if(bits[4].startswith("/challenge")):
				await queue.put(f"|/accept {other}")

			
async def out(queue, websocket):
	while True:
		token = await queue.get()
		await websocket.send(token)
		print(f">>> {token}")
		queue.task_done()
		
async def battle(queuein, queueout, str):
	while True:
		await asyncio.sleep(5)
		await queueout.put(f"{str}|/choose move 1")

async def main():
	queue = asyncio.Queue()
	uri = "ws://sim.smogon.com:8000/showdown/websocket"
	async with websockets.connect(uri) as websocket:
		await asyncio.gather(asyncio.create_task(inp(queue, websocket)),asyncio.create_task(out(queue, websocket)))


asyncio.run(main())
