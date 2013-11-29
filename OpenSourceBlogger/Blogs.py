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
    tag1 = db.StringProperty()
    tag2 = db.StringProperty()
    tag3 = db.StringProperty()
    tag4 = db.StringProperty()
    tag5 = db.StringProperty()
    thumbsup = db.IntegerProperty(default = 0)
    thumbsdown = db.IntegerProperty(default = 0)
    
application = webapp2.WSGIApplication([
    ('/Blogs.*',Blogs)
    ], debug=True)