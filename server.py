'''
A combination of tags and query will determine the nature of filter to be applied
This further enhancement will be made in the form of callable functions
Dear Students, Log in to Schoology and register yourself for the course "D1 Slot-CSE2004 Database Management Systems 2016: Morning Slot" using the access code X947K-6F2CH .
Upload the code using the Review II Document Upload Assignment Link. Every student should independently upload the code.
Mention your registration number,name, project name and team members name and registration number in the document that is uploaded. Regards Satish
'''


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
cur=db.cursor()

class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')

class LoginHandler(RequestHandler):
    def post(self):
       username=self.get_argument('username')
       password=self.get_argument('password')
       named_params={'Officer_id':str(username),
                     'password':str(password)}
       cur.execute('SELECT * FROM users WHERE Officer_id=:Officer_id AND password=:password',named_params)
       data=cur.fetchone()
       if not(data):
           #print 'not logged in'
           self.redirect('/?data=false')

       else:
           print 'data', str(data)
           print 'Logged in'
           self.set_secure_cookie('user', str(username))
           self.redirect('/dashboard')

class OfficerDashboardHandler(RequestHandler):
    def get(self):
        s=self.get_secure_cookie('user')
        if bool(s):
            named_params= dict(Officer_id=str(s))
            cur.execute('SELECT * FROM  Officer WHERE Officer_id=:Officer_id', named_params)
            data=cur.fetchone()
            if data:
                print 'data',data
                self.write(str(data))
            else:
                print 'no data found'
                self.write('record not found')

class CrimeQueryHandler(RequestHandler):
    def get(self):
        s=self.get_secure_cookie('user')
        if bool(s):
            tags=self.get_argument('tags')
            query=self.get_argument('query')


class LogoutHandler(RequestHandler):
    def get(self):
        if bool(self.get_secure_cookie('user')):
            self.clear_cookie('user')
            self.redirect('/?loggedOut=true')
        else:
            self.redirect('/?activeSession=false')
settings = dict(
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
cookie_secret="35an18y3-u12u-7n10-4gf1-102g23ce04n6",
        debug=True)

application=Application([
(r"/", IndexHandler),
(r"/login",LoginHandler),
(r"/dashboard",OfficerDashboardHandler),
(r"/logout",LogoutHandler)
],**settings)

if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.instance().start()