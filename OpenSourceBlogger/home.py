import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
from google.appengine.ext import db

class home(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('home.html') 
    
       self.response.write(template.render())
       
application = webapp2.WSGIApplication([
    ('/', home)
    ], debug=True)

