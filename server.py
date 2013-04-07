import tornado.ioloop 
import tornado.web
import tornado.websocket 
import tornado.httpserver
import yugioh
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
      print map(str,self.get_arguments("rfid"))
      if op:
	print op 
	print "DOPP"
      	op.write_message("poop")

application = tornado.web.Application([
    (r'/ws', WSHandler),
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

