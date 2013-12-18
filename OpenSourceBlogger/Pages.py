import cgi  
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Pages(db.Model):
    page_name = db.StringProperty(required = True)
    owner= db.StringProperty(required = True)
    create_time = db.DateTimeProperty(required = True)
    tags = db.StringProperty
    views = db.IntegerProperty(default = 0)
    
application = webapp2.WSGIApplication([
    ('/Pages.*',Pages)
    ], debug=True)