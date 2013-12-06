import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
from Comments import Comments
from UserLoggedin import UserLoggedIn
from google.appengine.ext import db

class showCompleteBlog(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('showCompleteBlog.html') 
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogid']
       session = urlparse.parse_qs(parsed_url.query)['sessionId']
       sessionId = int(session[0])
       
       login = 0
       user = ""
       username = ""
#       self.response.write(sessionId)
       try:
            user = UserLoggedIn.get_by_id(int(sessionId))
            username = user.blogger.nickname()
            login = 1
       except db.BadKeyError:
            login = 0
       except NameError:
            login = 0 
#       self.response.write(login) 
           
       b = Blogs.get_by_id(int(blogid[0]))
       
       query = "SELECT * FROM Comments WHERE blogid='"+blogid[0]+"'"
       comments_list = db.GqlQuery(query)
       count_comments = 0
       for c in comments_list:
           count_comments = count_comments + 1
       
       template_values = {'comments':comments_list,
                          'b': b,
                          'comment_count':count_comments,
                          'login' : login,
                          'cur_url' : cur_url,
                          'username' : username,
                          'sessionId' : sessionId
                          }
       
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/showCompleteBlog.*', showCompleteBlog)
    ], debug=True)

