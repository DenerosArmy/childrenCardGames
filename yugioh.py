import json 
D = True
class Card(object):
    TYPE_MONSTER = 0
    TYPE_SPELL = 2
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
        if not self.in_hand or self.field[location]:
            return False

        if self.in_hand.card_type == Card.TYPE_MONSTER:
            valid_locations = range(1,7)
        else:
            valid_locations = range(9,13)

        if location not in valid_locations:
            return False

        if D:
            print "Placing card " + str(self.in_hand) + " to  "+ str(location)

        self.field[location] = self.in_hand
        self.in_hand.state = state
        self.in_hand = None
        return True

    def can_remove(self, card):
        return False

    def remove(self, location, old_state):
        if self.field[location] is None or self.field[location].state != old_state:
            return False

        if self.in_hand != self.field[location]:
            # TODO: this assumes RFID scans before CV
            return False

        if not self.can_remove(self.in_hand):
            return False

        self.field[location] = None
        if self.in_hand.card_type == Card.TYPE_MONSTER:
            if D:
                print "monster removed from field"
        else:
            if D:
                print "magic card removed from field"
        self.in_hand = None
        return True

    def activate(self, location):
        if self.field[location] is None or self.field[location].state != "down":
            return False

        # TODO: effects of activating the card
        if D:
            print "card activated:", self.field[location]

        self.field[location].state = "att"
        return True
