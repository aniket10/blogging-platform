import cgi  
import webapp2
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Blogs(db.Model):
    ParentBlogId = db.IntegerProperty(required = True)
    owner= db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.BlobProperty(required = True)
    create_time = db.DateTimeProperty(required = True)
    modify_time = db.DateTimeProperty(required = True)
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