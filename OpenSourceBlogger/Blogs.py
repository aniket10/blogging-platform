import cgi  
import webapp2
import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Blogs(db.Model):
    owner= db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.BlobProperty(required = True)
    blog_time = db.TimeProperty(required = True)
    tags = db.StringProperty()
    
application = webapp2.WSGIApplication([
    ('/Blogs.*',Blogs)
    ], debug=True)