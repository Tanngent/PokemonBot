class Pokemon:
    def __init__(self):
        self.specie = 'null'
        self.level = 100
        self.health = 100
        self.move1 = 'null'
        self.move2 = 'null'
        self.move3 = 'null'
        self.move4 = 'null'
        self.atk = 0
        self.defe = 0
        self.spa = 0
        self.spd = 0
        self.spe = 0

    def update(self,json):
        print(json)
        self.specie = json['details']
        self.level = json['details']
        self.health = json['details']
        self.move1 = json['moves'][0]
        self.move2 = json['moves'][1]
        self.move3 = json['moves'][2]
        self.move4 = json['moves'][3]
        self.atk = json['stats']['atk']
        self.defe = json['stats']['def']
        self.spa = json['stats']['spa']
        self.spd = json['stats']['spd']
        self.spe = json['stats']['spe']

class Battle:
    def __init__(self):
        self.active = 1
        self.pokemon1 = Pokemon()
        self.pokemon2 = Pokemon()
        self.pokemon3 = Pokemon()
        self.pokemon4 = Pokemon()
        self.pokemon5 = Pokemon()
        self.pokemon6 = Pokemon()

    def update(self,json):
        print(json)
        print(json['side'])
        print(json['side']['pokemon'])
        i = 0
        while(not json['side']['pokemon'][i]['active']):
            i += 1
        self.active = i
        self.pokemon1.update(json['side']['pokemon'][0])
        self.pokemon2.update(json['side']['pokemon'][1])
        self.pokemon3.update(json['side']['pokemon'][2])
        self.pokemon4.update(json['side']['pokemon'][3])
        self.pokemon5.update(json['side']['pokemon'][4])
        self.pokemon6.update(json['side']['pokemon'][5])