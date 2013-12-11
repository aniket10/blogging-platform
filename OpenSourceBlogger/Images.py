import cgi  
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Images(db.Model):
    type= db.IntProperty(required = True)
    url = db.StringProperty()
    image = db.BlobProperty()
    
    
application = webapp2.WSGIApplication([
    ('/Images.*',Images)
    ], debug=True)