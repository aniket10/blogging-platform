import cgi  
import webapp2
import urlparse
from Comments import Comments

class addComment(webapp2.RequestHandler):

    def get(self):
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogid']
#       sessionid = urlparse.parse_qs(parsed_url.query)['sessionId']
       userid = urlparse.parse_qs(parsed_url.query)['user']
       comment_str = urlparse.parse_qs(parsed_url.query)['comment']    
       blog = blogid[0]
#       session = sessionid[0]
       user = userid[0]
       comment = comment_str[0]       
       
       l = Comments(owner = user,
                 blogid = blog,
                 comment = comment)
       l.put()
       self.redirect("/showCompleteBlog.py?blogid="+blog, False, False, None, None)
       



application = webapp2.WSGIApplication([
    ('/addComment.*',addComment)
    ], debug=True)



