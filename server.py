import tornado.ioloop 
import tornado.web
import tornado.websocket 
import tornado.httpserver
import yugioh
D = True
op = None
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        op = self
        if D:
            print "Opened Socket"
    def on_message(self,message):
        if D: 
            print 'message received %s' % message 

    
class RfidHandler(tornado.web.RequestHandler):
  def post(self):
      print map(str,self.get_arguments("rfid"))


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', RfidHandler),
])

if __name__ == "__main__":
    card = yugioh.Card("50003E4082AC","Dark Magician",0) 
    cards = {card.rfid:card}
    game = Game(cards,self.op)
    http_server = tornado.httpserver.HTTPServer(application) 
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start() 

