import cgi  
import webapp2
import urlparse
from google.appengine.ext import db
from google.appengine.api import urlfetch
from Blogs import Blogs


class addThumbsUp(webapp2.RequestHandler):

    def get(self):
       form = cgi.FieldStorage()
       
       blogId = form['blogid'].value
       url = form['dest_url'].value
 #      sessionId = int(form['sessionId'].value)
       b = Blogs.get_by_id(int(blogId))
       
       b.thumbsup = b.thumbsup + 1
       b.put()
           
       self.redirect(url, False, False, None, None)
 
application = webapp2.WSGIApplication([
    ('/addThumbsUp.*',addThumbsUp)
    ], debug=True)



