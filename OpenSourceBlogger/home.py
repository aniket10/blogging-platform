import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
from google.appengine.ext import db
from google.appengine.api import users

class home(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('home.html') 
    
       user = users.get_current_user()
       
       login = 0
       login_url = ""
       username = ""
       if user:
           login = 1
           username = user.nickname()
       else: 
           login = 0
           login_url = users.create_login_url('/')
       logout_url = users.create_logout_url('/')
    
       template_values = {'login' : login,
                          'login_url' : login_url,
                          'logout_url' : logout_url,
                          'username' : username  }                          
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/', home)
    ], debug=True)

