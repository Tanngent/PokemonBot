import random
import json
from Pokemon import Pokemon

class Battle:
    def __init__(self):
        self.ownId = ''
        self.enemyId = ''
        self.ownActive = 0
        self.enemyActive = 0

        self.ownTeam = [Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon()]
        self.enemyTeam = [Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon(), Pokemon()]

        self.forceSwitch = False
        self.trapped = False
        self.disabled = [False, False, False, False]
        
        self.ownTransform = -1
        self.enemyTransform = -1
        self.ownStatBoost = [0, 0, 0, 0]
        self.enemyStatBoost = [0, 0, 0, 0]

        self.parsableChanges = ['switch','move','-damage','-heal','faint','-status','-curestatus','-cureteam','-transform','-boost','-unboost',]

    def updateSelf(self,json):
        #print(json)
        #print(json['side'])
        #print(json['side']['pokemon'])

        #self.ownId = json['side']['id']
        #self.enemyId = 'p2' if self.ownId == 'p1' else 'p1'

        i = 0
        while(not json['side']['pokemon'][i]['active']):
            i += 1
        self.ownActive = i

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

    def parseChange(self,change,name):
        # print(change)
        for line in change:
            parts = line[1:].split('|')
            #print(parts[0])
            #print(len(parts))
            #if len(parts)>=3:
            #    print(parts[2])
            #    print(name)
            #    print(parts[2] == name)
            if parts[0] == 'player' and len(parts)>=3 and parts[2] == name:
                self.ownId = parts[1]
                self.enemyId = 'p2' if self.ownId == 'p1' else 'p1'
            if parts[0] == 'player' and len(parts)>=3 and parts[2] != name:
                self.enemyId = parts[1]
                self.ownId = 'p2' if self.enemyId == 'p1' else 'p1'
            if parts and parts[0] in self.parsableChanges:
                #print(line)
                isOwn = parts[1].startswith(self.ownId)
                inPokemon = parts[1].split(' ')[1]
                match parts[0]:
                    case 'switch':
                        #print(parts[1])
                        #print(isOwn)
                        #print(self.ownId)
                        if isOwn:
                            self.ownTransform = -1
                            self.ownStatBoost = [0, 0, 0, 0]
                        else:
                            self.enemyTransform = -1
                            self.enemyStatBoost = [0, 0, 0, 0]
                            inInfo = parts[2].split(',')
                            inPokemon = inInfo[0]
                            inLevel = 100 if len(inInfo)==1 else inInfo[1].translate(str.maketrans('', '', 'L '))
                            self.enemyActive = 0
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    break
                                if pk.specie == '':
                                    pk.specie = inPokemon
                                    pk.level = inLevel
                                    pk.getStats(inPokemon)
                                    break
                                self.enemyActive += 1
                    case 'move':
                        if not isOwn:
                            inMove = parts[2]
                            #print(inPokemon)
                            #print(inMove)
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    for i in range(4):
                                        if pk.moves[i] == inMove:
                                            break
                                        if pk.moves[i] == '':
                                            pk.moves[i] = inMove
                                            break
                                    break
                    case '-damage':
                        if not isOwn:
                            inHealth = 0.0 if parts[2] == '0 fnt' else int(parts[2].split(' ')[0].split('/')[0])/int(parts[2].split(' ')[0].split('/')[1])
                            #print(inPokemon)
                            #print(inHealth)
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    pk.health = inHealth
                                    break
                    case '-heal':
                        if not isOwn:
                            inHealth = 0.0 if parts[2] == '0 fnt' else int(parts[2].split(' ')[0].split('/')[0])/int(parts[2].split(' ')[0].split('/')[1])
                            #print(inPokemon)
                            #print(inHealth)
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    pk.health = inHealth
                                    break
                    case 'faint':
                        if not isOwn:
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    pk.health = 0.0
                                    pk.status = 'fnt'
                                    break
                    case '-status':
                        if not isOwn:
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    pk.status = parts[2]
                                    break
                    case '-curstatus':
                        if not isOwn:
                            for pk in self.enemyTeam:
                                if pk.specie == inPokemon:
                                    pk.status = ''
                                    break
                    case '-cureteam':
                        if not isOwn:
                            for pk in self.enemyTeam:
                                pk.status = ''
                    case '-transform':
                        if isOwn:
                            self.ownTransform = self.enemyActive
                        else:
                            self.enemyTransform = self.ownActive
                    case '-boost':
                        if not isOwn:
                            if parts[2] == 'atk':
                                self.enemyStatBoost[0] += int(parts[3])
                            if parts[2] == 'def':
                                self.enemyStatBoost[1] += int(parts[3])
                            if parts[2] == 'spa':
                                self.enemyStatBoost[2] += int(parts[3])
                            if parts[2] == 'spe':
                                self.enemyStatBoost[3] += int(parts[3])
                        if isOwn:
                            if parts[2] == 'atk':
                                self.ownStatBoost[0] += int(parts[3])
                            if parts[2] == 'def':
                                self.ownStatBoost[1] += int(parts[3])
                            if parts[2] == 'spa':
                                self.ownStatBoost[2] += int(parts[3])
                            if parts[2] == 'spe':
                                self.ownStatBoost[3] += int(parts[3])
                    case '-unboost':
                        if not isOwn:
                            if parts[2] == 'atk':
                                self.enemyStatBoost[0] -= int(parts[3])
                            if parts[2] == 'def':
                                self.enemyStatBoost[1] -= int(parts[3])
                            if parts[2] == 'spa':
                                self.enemyStatBoost[2] -= int(parts[3])
                            if parts[2] == 'spe':
                                self.enemyStatBoost[3] -= int(parts[3])
                        if isOwn:
                            if parts[2] == 'atk':
                                self.ownStatBoost[0] -= int(parts[3])
                            if parts[2] == 'def':
                                self.ownStatBoost[1] -= int(parts[3])
                            if parts[2] == 'spa':
                                self.ownStatBoost[2] -= int(parts[3])
                            if parts[2] == 'spe':
                                self.ownStatBoost[3] -= int(parts[3])
                    case _:
                        pass

    def getMove(self):
        validMoves = []
        validSwitches = []
        for i in range(6):
            if i != self.ownActive and self.ownTeam[i].status != 'fnt':
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
        
    def endBattle(self):
        with open('stats.json','r') as readFile:
            stats = json.load(readFile)
        for pk in self.ownTeam:
            if pk.specie not in stats:
                stats[pk.specie] = [pk.atk, pk.defe, pk.spa, pk.spd, pk.spe]
        with open('stats.json','w') as writeFile:
            json.dump(stats, writeFile, indent=4, sort_keys=True)

    def __str__(self):
        return 'Own Id: ' + str(self.ownId) + '\nEnemy Id: ' + str(self.enemyId) + '\n'\
        + self.ownTeam[0].__str__() + '\n' + self.ownTeam[1].__str__() + '\n' + self.ownTeam[2].__str__() + '\n' + self.ownTeam[3].__str__()\
             + '\n' + self.ownTeam[4].__str__() + '\n' + self.ownTeam[5].__str__() + '\nOwn Active: ' + str(self.ownActive) + '\nForce Switch: ' + str(self.forceSwitch)\
                + '\nTrapped: ' + str(self.trapped) + '\nOwn Transform: ' + str(self.ownTransform) + '\nDisabled: ' + str(self.disabled[0]) + ':' + str(self.disabled[1]) + ':' + str(self.disabled[2]) + ':' + str(self.disabled[3])\
                    + '\nOwn Stats: ' + str(self.ownStatBoost[0]) + ':' + str(self.ownStatBoost[1]) + ':' + str(self.ownStatBoost[2]) + ':' + str(self.ownStatBoost[3])\
                        + '\n' + self.enemyTeam[0].__str__() + '\n' + self.enemyTeam[1].__str__() + '\n' + self.enemyTeam[2].__str__() + '\n' + self.enemyTeam[3].__str__()\
                            + '\n' + self.enemyTeam[4].__str__() + '\n' + self.enemyTeam[5].__str__() + '\nEnemy Active: ' + str(self.enemyActive) + '\nEnemy Transform: ' + str(self.enemyTransform)\
                                + '\nEnemy Stats: ' + str(self.enemyStatBoost[0]) + ':' + str(self.enemyStatBoost[1]) + ':' + str(self.enemyStatBoost[2]) + ':' + str(self.enemyStatBoost[3])

    def getState(self):
        val = ""
        if self.ownTransform == -1:
            val = val + self.ownTeam[self.ownActive].__str__() + ","
        else:
            val = val + self.enemyTeam[self.ownTransform].__str__() + ","
        for i in range(6):
            if i != self.ownActive:
                val = val + self.ownTeam[i].__str__() + ","
        
        if self.enemyTransform == -1:
            val = val + self.enemyTeam[self.enemyActive].__str__() + ","
        else:
            val = val + self.ownTeam[self.enemyTransform].__str__() + ","
        for i in range(6):
            if i != self.enemyActive:
                val = val + self.enemyTeam[i].__str__() + ","
        val = val + str(self.ownStatBoost[0]) + "," + str(self.ownStatBoost[1]) + "," + str(self.ownStatBoost[2]) + "," + str(self.ownStatBoost[3]) + ","
        val = val + str(self.ownStatBoost[0]) + "," + str(self.ownStatBoost[1]) + "," + str(self.ownStatBoost[2]) + "," + str(self.ownStatBoost[3])
        return val
    
    def getHealthDelta(self):
        ownHealth = 0
        ownAlive = 0
        enemyHealth = 0
        enemyAlive = 0
        for i in range(6):
            ownHealth += self.ownTeam[i].health
            ownAlive += 1 if self.ownTeam[i].health > 0 else 0
            enemyHealth += self.enemyTeam[i].health
            enemyAlive += 1 if self.enemyTeam[i].health > 0 else 0
        print(ownHealth)
        print(ownAlive)
        print(enemyHealth)
        print(enemyAlive)
        print(ownHealth + ownAlive - enemyHealth - enemyAlive)
        return ownHealth + ownAlive - enemyHealth - enemyAlive