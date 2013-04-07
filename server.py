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
      rfid = self.get_arguments("rfid")

      if rfid:
	tag = rfid[0]
      print tag
      game.pick_up(tag)
      if op:
	print op 
	print "DOPP"

class CVHandler(tornado.web.RequestHandler):
  def post(self):
      position = int(self.get_argument("position"))
      old = self.get_argument("old")
      new = self.get_argument("new")
      if game and game.place(position,new):
        print "SENDING MESSAGE"
        op.write_message(json.dumps(map(yugioh.serialize,game.field)))
      print "Detected class change at {} from '{}' to {}'".format(position, old, new)

application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/cv', CVHandler),
    (r'/', RfidHandler),
])

if __name__ == "__main__":
    card0 = yugioh.Card("50003E4082AC","Dark Magician",0) 
    card1 = yugioh.Card("67007264C9B8", "Blue Eyes White Dragon", 0)
    card2 = yugioh.Card("67007262ED9A", "Mirror Force", 2)   
    card3 = yugioh.Card("67007274CDAC","Exodia",0) 	
    cards = {eval("card"+str(i)).rfid:eval("card"+str(i)) for i in range(4)}	

    http_server = tornado.httpserver.HTTPServer(application) 
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start() 

