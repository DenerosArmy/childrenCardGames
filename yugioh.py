D = True
class Card(object):
    def __init__(self,rfid_id, card_name,card_type):
        self.rfid = rfid_id
        self.name = card_name 
        self.card_type = card_type 
        self.position = None 
        self.state = "deck" 
    def __str__(self):
        return (self.name,self.position,self.state)

class Field(object):
    def __init__(self):
        self.monsters = [] 
        self.spraps = [] 
        self.graveyard = [] 
        self.field_card = None 

    def update(self,field): 
        self.field = field[0] 
        self.monsters = field[1:6]  
        self.graveyard = field[6] 
        self.spraps = field[8:12]

class Game(object):
    def __init__(self,cards,function=str):
        self.cards = {} 
        self.field = Field()
        self.in_hand = None
        self.function = function
        self.mat 
    def pick_up(self,id): 
        if D:
            print "Picked up " + self.cards[id] 
    
    def place(self,location,postion):
        if self.in_hand:
            if D:
                print "Placing card to " + str(location) 
            #self.function(str(self.in_hand),location,position)
            
