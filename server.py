import tornado.ioloop 
import tornado.web
import tornado.websocket 
import tornado.httpserver
import yugioh
import json 
D = True
op = None
game = None

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global game
        global op
        op = self
        game = yugioh.Game(cards,op.write_message)
        if D:
            print "Opened Socket"
    def on_message(self,message):
        if D: 
            print 'message received %s' % message 

    
class RfidHandler(tornado.web.RequestHandler):
    def post(self):
        global game
        rfid = self.get_arguments("rfid")

        if rfid:
            tag = rfid[0]
            print tag
            game.pick_up(tag)
        if op:
            print op 
            print "DOPP"
class AttackHandler(tornado.web.RequestHandler):
    def get(self):
        op.write_message("ATTACK")


class CVHandler(tornado.web.RequestHandler):
  def post(self):
      position = int(self.get_argument("position"))
      old = self.get_argument("old")
      new = self.get_argument("new")
      print "Detected class change at {} from '{}' to '{}'".format(position, old, new)
      if not game:
          return

      have_update = False
      if old == "none" and new in ["down", "att"]:
          have_update = game.place(position, new)
          if not have_update and new == "att":
              have_update = game.activate(position)
      elif old in ["down", "att"] and new == "none":
          have_update = game.remove(position, old)
      elif old == "down" and new == "att":
          have_update = game.activate(position)
      elif old == "att" and new == "down":
          have_update = False # cannot make face-up card become face-down

      if have_update:
        print "SENDING MESSAGE"
        op.write_message(json.dumps(map(yugioh.serialize,game.field)))

application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/attack', AttackHandler),
    (r'/cv', CVHandler),
    (r'/', RfidHandler),
])

if __name__ == "__main__":
    card0 = yugioh.Card("50003E4082AC","Dark Magician",yugioh.Card.TYPE_MONSTER)
    card1 = yugioh.Card("67007264C9B8", "Blue Eyes White Dragon", yugioh.Card.TYPE_MONSTER)
    card2 = yugioh.Card("67007262ED9A", "Mirror Force", yugioh.Card.TYPE_SPELL)
    card3 = yugioh.Card("67007274CDAC","Exodia",yugioh.Card.TYPE_MONSTER)
    cards = {eval("card"+str(i)).rfid:eval("card"+str(i)) for i in range(4)}

    http_server = tornado.httpserver.HTTPServer(application) 
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start() 

