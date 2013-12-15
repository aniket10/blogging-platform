import cgi  
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

class TempStore(db.Model):
    ParentBlogId = db.IntegerProperty(required = True)
    owner= db.StringProperty(required = True)
    title = db.StringProperty()
    content = db.BlobProperty()
    tag = db.StringProperty()
    
    
application = webapp2.WSGIApplication([
    ('/TempStore.*',TempStore)
    ], debug=True)