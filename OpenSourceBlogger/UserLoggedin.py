import cgi  
import webapp2
import datetime
from google.appengine.ext import db
from google.appengine.api import users

class UserLoggedIn(db.Model):
    blogger= db.UserProperty(required = True)
    
application = webapp2.WSGIApplication([
    ('/UserLoggedIn.*',UserLoggedIn)
    ], debug=True)