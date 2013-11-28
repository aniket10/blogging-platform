import webapp2
import cgi
import jinja2
import os
from Blogs import Blogs
from google.appengine.ext import db

class BlogFeed(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('BlogFeed.html')
        
       blog_owner = 'aniket'
       blogs = db.GqlQuery("SELECT * FROM Blogs WHERE owner = '"+blog_owner+"' ORDER BY blog_time DESC")
       
       count = 0
       subset_blogs = []
       for b in blogs:       
           if count < 2:
               subset_blogs.append(b)
               count = count+1
               continue
           template_values = {
                'blogs': subset_blogs,
                'blog_owner': blog_owner,
            }
          
           self.response.write(template.render(template_values))
           count = 0
           subset_blogs = []
           
           
application = webapp2.WSGIApplication([
    ('/BlogFeed.*', BlogFeed)
    ], debug=True)

