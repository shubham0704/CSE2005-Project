__author__ = 'SHUBHAM'
#tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer


import os
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import cx_Oracle



db=cx_Oracle.connect('system','master','localhost:1521/XE')
cursor=db.cursor()

class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class LoginHandler(RequestHandler):
    def post(self):
       flag=1
       username=self.get_argument('username')
       password=self.get_argument('password')
       named_params={'username':str(username),
                     'password':str(password)}
       cursor.execute('SELECT * from users WHERE username=:username AND password=:password',named_params)
       data=cursor.fetchone()
       print 'data',data
       if not(data):
           print 'not logged in'
           self.redirect('/')

       else:
           print 'Logged in'
           self.redirect('/dashboard')


settings = dict(
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug=True)

application=Application([
(r"/", IndexHandler),
(r"/login",LoginHandler)
],**settings)

if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.instance().start()