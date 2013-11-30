import cgi  
import webapp2
import urlparse
from google.appengine.ext import db
from Blogs import Blogs


class addThumbsDown(webapp2.RequestHandler):

    def get(self):
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogid']
       userid = urlparse.parse_qs(parsed_url.query)['user'] 
       blog = blogid[0]
       user = userid[0]
       b = Blogs.get_by_id(int(blogid[0]))
       
       b.thumbsdown = b.thumbsdown + 1
       b.put()
       
       self.redirect("/showCompleteBlog.py?blogid="+blog, False, False, None, None)
       



application = webapp2.WSGIApplication([
    ('/addThumbsDown.*',addThumbsDown)
    ], debug=True)



