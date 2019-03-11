#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import datetime
import os
from caching import Cache
from time import sleep

DEBUG = os.getenv("DEBUG", False)
redisHost = os.getenv("REDISHOST", "127.0.0.1")
redisPort = os.getenv("REDISPORT", 6379)
redisDB = os.getenv("REDISDB", 0)
globalExpiry = os.getenv("GLOBALEXPIRY", 5)
maxKeys = os.getenv("MAXKEYS", 5)
httpPort = os.getenv("HTTPPORT", 8888)

cache = Cache()
cache.setDebug(DEBUG)
cache.setRedis(redisHost, redisPort, redisDB)
cache.setExpiry(globalExpiry)
cache.setMaxKeys(maxKeys)

class HelpHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is the help message, it is not really helpful. Read the README.")

class GetHandler(tornado.web.RequestHandler):
    def get(self, key):
        data = cache.get(key)
        if data:
            self.write(data.read())
        else:
            self.set_status(500)
            self.write("Error")
        sleep(1)

class DumpHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(str(cache))

def main():
    app = tornado.web.Application([
        (r"/", HelpHandler),
        (r"/get/?", HelpHandler),
        (r"/get/(.*)", GetHandler)
    ])
    if DEBUG:
        app.add_handlers(r".*", [ (r"/dump", DumpHandler) ])
    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(port=httpPort, reuse_port=True)
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    print("Proxy starting up")
    main()