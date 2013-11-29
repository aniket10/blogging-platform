import cgi  
import webapp2
import urlparse
from Likes import Likes
    


class addLike(webapp2.RequestHandler):

    def get(self):
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogid']
       userid = urlparse.parse_qs(parsed_url.query)['user']  
       blog = blogid[0]
       user = userid[0]       
       
       l = Likes(owner = user,
                 blogid = blog)
       l.put()
       self.redirect("/showCompleteBlog.py?blogid="+blog, False, False, None, None)
       



application = webapp2.WSGIApplication([
    ('/addLike.*',addLike)
    ], debug=True)



