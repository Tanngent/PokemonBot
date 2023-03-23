import asyncio
import websockets
import requests
import json

from Battle import Battle

async def inp(queue, websocket): # accept incoming websocket message
	url = 'https://play.pokemonshowdown.com/~~showdown/action.php'
	greeting = await websocket.recv()
	# print(f'<<< {greeting}')
	# wait for challstr
	while not greeting.startswith('|challstr|'):
		greeting = await websocket.recv()
		# print(f'<<< {greeting}')
	f = open('user.txt','r')
	usname = f.readline()
	passwd = f.readline()
	header = {'Content-type': 'application/x-www-form-urlencoded; encoding=UTF-8'}
	content = {'act': 'login', 'name': usname[:-1],'pass': passwd, 'challstr': greeting[10:]}
	# send the login request
	r = requests.post(url,data=content,headers=header)
	s = json.loads(r.text[1:])
	l = '|/trn ' + usname[0:-1] +',0,' + s['assertion']
	# put the assertion 
	await queue.put(l)
	games = {}
	while True:
		greeting = await websocket.recv()
		print(f'<<< {greeting}')
		if greeting.startswith('|updatesearch|'): # new game started or game stopped
			s = json.loads(greeting[14:])
			localgames = list(games)
			remotegames = None
			if s['games']: # this will exist if there is a game going on
				remotegames = list(s['games'])
			else:
				remotegames = []
			startedgames = set(remotegames) - set(localgames)
			endedgames = set(localgames) - set(remotegames)
			for game in startedgames: # games that just started
				battlequeue = asyncio.Queue()
				asyncio.gather(asyncio.create_task(battle(battlequeue,queue,game,usname)))
				games[game] = battlequeue
				await queue.put(f'|/join {game}')
			for game in endedgames: # games taht just ended
				await games.get(game).put('end')
				games.pop(game,None)
				await queue.put(f'|/leave {game}')
			#if len(games) == 0:
				# await queue.put('|/challenge 0hzlf9ccsl, gen1randombattle')
		elif greeting.startswith('|pm|'): # pm, including challenge request
			bits = greeting.split('|')
			other = bits[2].strip()
			if bits[4].startswith('/challenge'): # accept challenges
				await queue.put(f'|/accept {other}')
		elif greeting.startswith('>battle'): # message to a specific battle
			gamename = greeting.partition('\n')[0][1:]
			if gamename in games:
				await games[gamename].put(greeting)
			else:
				print(f'Battle with name {gamename} does not exist or has already ended\n')

async def out(queue, websocket): # send websocket message
	while True:
		token = await queue.get()
		await websocket.send(token)
		print(f'>>> {token}')
		queue.task_done()

async def battle(queuein, queueout, string, usname): # battle function for handling messaging
	print(f'Started {string}')
	thisBattle = Battle()
	receivedRequest = False
	receivedChange = False
	savedStates = []
	savedDecision = []
	savedHP = []
	while True:
		if queuein.empty():
			# await queueout.put(f'{str}|/choose move 1')
			await asyncio.sleep(1)
		else:
			token = await queuein.get()
			if token == 'end': # end battle
				thisBattle.endBattle()
				return
			else:
				# print(f'<<< {token}')
				lines = token.split('\n')[1:]
				if lines[0].startswith('|request|') and lines[0] != '|request|': # request for move
					# print('receivedRequest')
					# print(lines[0][9:])
					teaminfo = json.loads(lines[0][9:])
					thisBattle.updateSelf(teaminfo)
					receivedRequest = True
				elif lines[0] == '|' or '|start' in lines: # battle update
					# print('receivedChange')
					thisBattle.parseChange(lines, usname.strip())
					receivedChange = True
				if receivedRequest and receivedChange: # received both, update previous decision outcome, make decision
					move = thisBattle.getMove()
					savedStates.append(thisBattle.getState())
					savedDecision.append(move)
					savedHP.append(thisBattle.getHealthDelta())
					if len(savedStates) > 3:
						myString = savedStates[0]
						myString = myString + "," + savedDecision[0]
						myString = myString + "," +str(savedHP[1]-savedHP[0] + 0.5*(savedHP[2]-savedHP[1]) + 0.25*(savedHP[3]-savedHP[2])) + "\n"
						print(savedHP[0])
						print(savedHP[1])
						print(savedHP[2])
						print(savedHP[3])
						print(savedHP[1]-savedHP[0] + 0.5*(savedHP[2]-savedHP[1]) + 0.25*(savedHP[3]-savedHP[2]))
						myFile = open("train.csv",mode="a")
						myFile.write(myString)
						myFile.close()
						savedStates.pop(0)
						savedDecision.pop(0)
						savedHP.pop(0)
					await queueout.put(f'{string}|/choose {move}')
					receivedRequest = False
					receivedChange = False

async def main(): # program main
	queue = asyncio.Queue()
	uri = 'ws://sim.smogon.com:8000/showdown/websocket'
	async with websockets.connect(uri) as websocket:
		await asyncio.gather(asyncio.create_task(inp(queue, websocket)),asyncio.create_task(out(queue, websocket)))


asyncio.run(main())
