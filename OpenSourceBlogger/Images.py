import cgi  
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Images(db.Model):
    owner = db.StringProperty(required=True)
    image_url = db.StringProperty()
    image_key = db.StringProperty()    
    
application = webapp2.WSGIApplication([
    ('/Images.*',Images)
    ], debug=True)