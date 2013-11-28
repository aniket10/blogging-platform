import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
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
       b = Blogs.get_by_id(int(blogid[0]))
       
       template_values = {
            'b': b,
       }
       
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/showCompleteBlog.*', showCompleteBlog)
    ], debug=True)

