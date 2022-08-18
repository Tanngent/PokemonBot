import random


class Pokemon:
    def __init__(self):
        self.specie = ''
        self.level = 0
        self.health = 100
        self.condition = ''
        self.moves = ['','','','']
        self.atk = 0
        self.defe = 0
        self.spa = 0
        self.spd = 0
        self.spe = 0

    # Update state of party pokemon from JSON
    def update(self,json):
        #print(json)
        self.specie = json['details'].split(' ')[0].translate(str.maketrans('', '', ', '))
        self.level = 100 if len(json['details'].split(' ')) == 1 else json['details'].split(' ')[1].translate(str.maketrans('', '', 'L, '))
        self.health = 0.0 if json['condition'].split(' ')[0] == '0' else int(json['condition'].split(' ')[0].split('/')[0])/int(json['condition'].split(' ')[0].split('/')[1])
        self.condition = '' if len(json['condition'].split(' ')) == 1 else json['condition'].split(' ')[1]
        self.moves[0] = json['moves'][0]
        self.moves[1] = '' if len(json['moves']) <= 1 else json['moves'][1]
        self.moves[2] = '' if len(json['moves']) <= 2 else json['moves'][2]
        self.moves[3] = '' if len(json['moves']) <= 3 else json['moves'][3]
        self.atk = json['stats']['atk']
        self.defe = json['stats']['def']
        self.spa = json['stats']['spa']
        self.spd = json['stats']['spd']
        self.spe = json['stats']['spe']

    # Update state of enemy pokemon from text
    def parseChange(self,change):
        pass
        # TODO parse

    def __str__(self):
        return str(self.specie) + ', ' + str(self.level) + ', ' + str(self.health) + ', ' + self.condition + ', ' + self.moves[0]\
            + ', ' + self.moves[1] + ', ' + self.moves[2] + ', ' + self.moves[3] + ', ' + str(self.atk) + ', ' + str(self.defe)\
                 + ', ' + str(self.spa)  + ', ' + str(self.spd)  + ', ' + str(self.spe)


class Battle:
    def __init__(self):
        self.player = ''
        self.active = 1
        self.ownTeam = [Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon()]
        self.enemyTeam = [Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon()]
        self.forceSwitch = False
        self.trapped = False
        self.disabled = [False, False, False, False]

    def updateSelf(self,json):
        #print(json)
        #print(json['side'])
        #print(json['side']['pokemon'])
        self.player = json['side']['id']

        i = 0
        while(not json['side']['pokemon'][i]['active']):
            i += 1
        self.active = i

        self.ownTeam[0].update(json['side']['pokemon'][0])
        self.ownTeam[1].update(json['side']['pokemon'][1])
        self.ownTeam[2].update(json['side']['pokemon'][2])
        self.ownTeam[3].update(json['side']['pokemon'][3])
        self.ownTeam[4].update(json['side']['pokemon'][4])
        self.ownTeam[5].update(json['side']['pokemon'][5])
        self.forceSwitch = 'forceSwitch' in json
        self.trapped = False
        if('active' in json):
            self.disabled[0] = False if 'disabled' not in json['active'][0]['moves'][0] else json['active'][0]['moves'][0]['disabled']
            self.disabled[1] = True if len(json['active'][0]['moves']) <= 1 else json['active'][0]['moves'][1]['disabled']
            self.disabled[2] = True if len(json['active'][0]['moves']) <= 2 else json['active'][0]['moves'][2]['disabled']
            self.disabled[3] = True if len(json['active'][0]['moves']) <= 3 else json['active'][0]['moves'][3]['disabled']
            self.trapped = 'trapped' in json['active'][0]

    def getMove(self):
        validMoves = []
        validSwitches = []
        for i in range(6):
            if i != self.active and self.ownTeam[i].condition != 'fnt':
                validSwitches.append('switch ' + str(i + 1))
        switchChoice = -1 if len(validSwitches) == 0 else random.randint(0, len(validSwitches) - 1)
        #print(validSwitches)
        #print(switchChoice)
        for i in range(4):
            if not self.disabled[i]:
                validMoves.append('move ' + str(i + 1))
        moveOrSwitch = random.randint(1, 10)
        moveChoice = random.randint(0, len(validMoves) - 1)
        #print(validMoves)
        #print(moveChoice)
        #print(moveOrSwitch)
        if not self.trapped and switchChoice != -1 and (self.forceSwitch or moveOrSwitch > 6):
            return validSwitches[switchChoice]
        else:
            return validMoves[moveChoice]
        


    def __str__(self):
        return self.ownTeam[0].__str__() + '::\n' + self.ownTeam[1].__str__() + '::\n' + self.ownTeam[2].__str__() + '::\n' + self.ownTeam[3].__str__()\
             + '::\n' + self.ownTeam[4].__str__() + '::\n' + self.ownTeam[5].__str__() + '::\n' + str(self.active) + '::\n' + str(self.forceSwitch)\
                + '::\n' + str(self.disabled[0]) + '::\n' + str(self.disabled[1]) + '::\n' + str(self.disabled[2]) + '::\n' + str(self.disabled[3])\
                    + '::\n' + self.enemyTeam[0].__str__() + '::\n' + self.enemyTeam[1].__str__() + '::\n' + self.enemyTeam[2].__str__() + '::\n' + self.enemyTeam[3].__str__()\
                        + '::\n' + self.enemyTeam[4].__str__() + '::\n' + self.enemyTeam[5].__str__()