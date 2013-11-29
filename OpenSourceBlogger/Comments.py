import cgi  
import webapp2
import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Comments(db.Model):
    owner= db.StringProperty(required = True)
    blogid = db.StringProperty(required = True)
    comment = db.StringProperty(required = True)
    
application = webapp2.WSGIApplication([
    ('/Comments.*',Comments)
    ], debug=True)