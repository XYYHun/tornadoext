
import tornado.ioloop
import tornado.web

from tornadoext.ramsession import RamSession

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        session = RamSession(self)
        if session['times'] == None :
            session['times'] = 0
        session['times'] = session['times'] + 1
        self.write("Hello, %s" % session['times'])

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
