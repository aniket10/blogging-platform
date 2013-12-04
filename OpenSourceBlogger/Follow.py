import cgi  
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Follow(db.Model):
    item= db.StringProperty(required = True)
    user = db.StringProperty(required = True)
    type = db.IntegerProperty(required = True)
    
    
application = webapp2.WSGIApplication([
    ('/Follow.*',Follow)
    ], debug=True)