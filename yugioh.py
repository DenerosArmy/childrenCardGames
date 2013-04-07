import json 
D = True
class Card(object):
    def __init__(self,rfid_id, card_name,card_type):
        self.rfid = rfid_id
        self.name = card_name 
        self.card_type = card_type 
        self.position = None 
        self.state = "deck" 
    def serialize(self):
        if not self:
            return
        return ({"name":self.name,"state":self.state})

    
class Game(object):
    def __init__(self,cards,function=str):
        self.cards = {} 
        self.field = [None for _ in range(14)]
        self.in_hand = None
        self.function = function
    def pick_up(self,id): 
        if D:
            print "Picked up " + self.cards[id] 
    
    def place(self,location,postion):
        if self.in_hand:
            if D:
                print "Placing card to " + str(location) 
            self.field[position] = self.in_hand
        self.function(map(Card.serialize,self.field))

 
