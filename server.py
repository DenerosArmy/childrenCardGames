import tornado.ioloop 
import tornado.web
import tornado.websocket 
import tornado.httpserver
import yugioh
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Hello World")

    def on_message(self,message):
        print 'message received %s' % message 

    def on_close(self):
        print 'connection closed'
class RfidHandler(tornado.web.RequestHandler):
  def get(self,**kwargs):
      print map(str,self.get_arguments("penis"))[0]
  def post(self):
    self.write("Hello, chatter! [POST]")


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', RfidHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application) 
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start() 

