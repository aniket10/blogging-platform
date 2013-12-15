import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
from Comments import Comments
from Pages import Pages
from UserLoggedin import UserLoggedIn
from google.appengine.ext import db
from google.appengine.api import users 

class viewAllBlogs(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('viewAllBlogs.html') 
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blog = urlparse.parse_qs(parsed_url.query)['name']
#       session = urlparse.parse_qs(parsed_url.query)['sessionId']
#       sessionId = int(session[0])
       blogname = blog[0]
       
       login = 0
       user = ""
       username = ""
#       self.response.write(sessionId)
#       try:
#            user = UserLoggedIn.get_by_id(int(sessionId))
#            username = user.blogger.nickname()
#            login = 1
#       except db.BadKeyError:
#            login = 0
#       except NameError:
#            login = 0 
#       self.response.write(login) 
       user = users.get_current_user()
       if user:
            login = 1
            username = user.nickname()
       else:
            login = 0
            login_url = users.create_login_url(cur_url)
       logout_url = users.create_logout_url('/')

           
       query = "SELECT * FROM Pages WHERE page_name='"+blogname+"'"
       blogs_list = db.GqlQuery(query)
       
       self.response.write('Printing result')
       for b in blogs_list:
           self.response.write(b.owner) 
       
       template_values = { 
                          'blogs_list': blogs_list,
#                          'sessionId' : sessionId,
                          'name' : blogname,
                          'login' : login,
                          'cur_url' : cur_url,
                          'username' : username,
                          }
       
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/viewAllBlogs.*', viewAllBlogs)
    ], debug=True)

