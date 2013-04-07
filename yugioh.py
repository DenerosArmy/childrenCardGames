import json 
D = True
class Card(object):
    def __init__(self,rfid_id, card_name,card_type,attack=0,defense=0):
        self.rfid = rfid_id
        self.name = card_name 
        self.card_type = card_type 
        self.attack = attack 
        self.defense = defense
        self.position = None 
	
        self.state = "deck" 
    def __str__(self):
	return str(serialize(self))
def serialize(card):
    if not card:
       return
    return ({"name":card.name,"state":card.state})

    
class Game(object):
    def __init__(self,cards,function=str):
        self.cards = cards
        self.field = [None for _ in range(14)]
        self.op_field = [None for _ in range(14)]
        self.in_hand = None
        self.function = function
         
    def pick_up(self,id): 
        if D:
            print "Picked up " + str(self.cards.get(id))
	print self.cards 
	self.in_hand = self.cards.get(id) 
	 
     
    def place(self,location,state):
        if self.in_hand and int(location) < 13:
	    valid = False
	    if self.in_hand.card_type == 0: 
		valid = location in [i for i in range(1,7)] 
	    else:
		valid = location in [i for i in range(9,13)] 
            if not valid:
		return False
            if D:
                print "Placing card " + str(self.in_hand) + " to  "+ str(location) 
	    
            print self.field	

            self.field[location] = self.in_hand	
            self.in_hand.state = state
	    self.in_hand = None
	    return True
    	return False 
